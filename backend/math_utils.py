"""Deterministic math utilities for CFP-AI"""
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta


def calculate_monthly_surplus(income: float, expenses: float) -> Decimal:
    """Calculate monthly surplus"""
    return Decimal(str(income)) - Decimal(str(expenses))


def calculate_amortization(principal: float, apr: float, months: int) -> Decimal:
    """
    Calculate monthly payment for amortizing loan
    
    Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    """
    P = Decimal(str(principal))
    r = Decimal(str(apr)) / Decimal('12')  # Monthly rate
    n = Decimal(str(months))
    
    if r == 0:
        return P / n
    
    numerator = r * (1 + r) ** n
    denominator = (1 + r) ** n - 1
    
    monthly_payment = P * (numerator / denominator)
    return monthly_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_snowball_payoff(balances: List[Dict[str, Any]], monthly_surplus: float) -> List[Dict[str, Any]]:
    """
    Snowball method: Pay minimum on all, extra on smallest balance
    
    Returns: List of payoff schedule entries
    """
    # Sort by balance (smallest first)
    sorted_balances = sorted(balances, key=lambda x: x['balance'])
    
    schedule = []
    surplus = Decimal(str(monthly_surplus))
    current_date = datetime.now()
    
    for idx, balance in enumerate(sorted_balances):
        payment = Decimal(str(balance.get('min_payment', balance['balance'] * 0.02)))
        total_payment = payment + surplus
        
        # Calculate payment date (staggered by month)
        payment_date = current_date + timedelta(days=idx * 30)
        
        schedule.append({
            "account": balance['name'],
            "payment": float(total_payment),
            "balance": balance['balance'],
            "date": payment_date.strftime('%Y-%m-%d')
        })
        
        # After this debt is paid, all its payment goes to next
        surplus = total_payment
    
    return schedule


def calculate_avalanche_payoff(balances: List[Dict[str, Any]], monthly_surplus: float) -> List[Dict[str, Any]]:
    """
    Avalanche method: Pay minimum on all, extra on highest APR
    
    Returns: List of payoff schedule entries
    """
    # Sort by APR (highest first)
    sorted_balances = sorted(balances, key=lambda x: x['apr'], reverse=True)
    
    schedule = []
    surplus = Decimal(str(monthly_surplus))
    current_date = datetime.now()
    
    for idx, balance in enumerate(sorted_balances):
        payment = Decimal(str(balance.get('min_payment', balance['balance'] * 0.02)))
        total_payment = payment + surplus
        
        # Calculate payment date (staggered by month)
        payment_date = current_date + timedelta(days=idx * 30)
        
        schedule.append({
            "account": balance['name'],
            "payment": float(total_payment),
            "balance": balance['balance'],
            "apr": balance['apr'],
            "date": payment_date.strftime('%Y-%m-%d')
        })
        
        surplus = total_payment
    
    return schedule


def generate_savings_schedule(goal_amount: float, deadline_days: int, monthly_surplus: float) -> List[Dict[str, str]]:
    """
    Generate micro-savings schedule to reach goal
    
    Returns: List of {date, amount} entries
    """
    goal = Decimal(str(goal_amount))
    surplus = Decimal(str(monthly_surplus))
    
    # Calculate required savings per month
    months = Decimal(str(deadline_days)) / Decimal('30')
    monthly_savings = goal / months
    
    # Break into weekly micro-deposits
    weekly_savings = monthly_savings / Decimal('4')
    
    schedule = []
    current_date = datetime.now()
    total_saved = Decimal('0')
    
    week = 0
    while total_saved < goal:
        save_date = current_date + timedelta(weeks=week)
        amount = min(weekly_savings, goal - total_saved)
        
        schedule.append({
            "date": save_date.strftime('%Y-%m-%d'),
            "amount": float(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        })
        
        total_saved += amount
        week += 1
        
        if week > 200:  # Safety limit
            break
    
    return schedule


def calculate_credit_utilization(balance: float, limit: float) -> Decimal:
    """
    Calculate credit utilization percentage
    """
    if limit == 0:
        return Decimal('0')
    
    utilization = (Decimal(str(balance)) / Decimal(str(limit))) * Decimal('100')
    return utilization.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def generate_checksum(data: Dict[str, Any]) -> str:
    """
    Generate deterministic checksum for calculations
    
    This ensures same input always produces same output
    """
    # Sort keys for deterministic ordering
    json_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_str.encode()).hexdigest()


def calculate_dti(monthly_debt_payments: float, gross_monthly_income: float) -> Decimal:
    """
    Calculate Debt-to-Income ratio
    """
    if gross_monthly_income == 0:
        return Decimal('999')  # Undefined, but flagged
    
    dti = (Decimal(str(monthly_debt_payments)) / Decimal(str(gross_monthly_income))) * Decimal('100')
    return dti.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
