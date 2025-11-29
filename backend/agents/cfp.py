"""CFP-AI - Deterministic financial math and verification engine"""
from fastapi import APIRouter, HTTPException
import logging

from schemas import (
    CFPSimulateInput,
    CFPSimulateOutput,
    CFPVerifyInput,
    CFPVerifyOutput,
    CFPCalculations,
    SavingsScheduleEntry,
    PaydownScheduleEntry
)
from math_utils import (
    calculate_monthly_surplus,
    calculate_snowball_payoff,
    calculate_avalanche_payoff,
    generate_savings_schedule,
    generate_checksum,
    calculate_dti
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cfp", tags=["cfp"])

# CFP engine version
CFP_VERSION = "v1.0"


@router.post("/simulate", response_model=CFPSimulateOutput)
async def simulate_scenario(input_data: CFPSimulateInput):
    """
    Deterministic financial simulation
    
    Calculates:
    - Monthly surplus
    - Savings plan
    - Debt payoff schedule (snowball method)
    - Emergency fund projections
    """
    try:
        scenario = input_data.scenario
        
        # Calculate monthly surplus
        monthly_surplus = float(calculate_monthly_surplus(
            scenario.income,
            scenario.expenses
        ))
        
        # Generate savings plan if goal provided
        savings_plan = []
        if scenario.goal and scenario.goal.type == "emergency":
            schedule = generate_savings_schedule(
                scenario.goal.amount,
                scenario.goal.deadline_days,
                monthly_surplus
            )
            savings_plan = [SavingsScheduleEntry(**entry) for entry in schedule]
        
        # Generate payoff schedule if balances provided
        paydown_schedule = []
        if scenario.balances:
            schedule = calculate_snowball_payoff(
                [b.model_dump() for b in scenario.balances],
                monthly_surplus * 0.5  # Allocate 50% to debt, 50% to savings
            )
            paydown_schedule = [PaydownScheduleEntry(**entry) for entry in schedule]
        
        # Create calculations object
        calculations = CFPCalculations(
            monthly_surplus=monthly_surplus,
            savings_plan=savings_plan,
            paydown_schedule=paydown_schedule
        )
        
        # Generate checksum for verification
        checksum_data = {
            "income": scenario.income,
            "expenses": scenario.expenses,
            "monthly_surplus": monthly_surplus,
            "cfp_version": CFP_VERSION
        }
        checksum = generate_checksum(checksum_data)
        
        # Assumptions
        assumptions = [
            "30-day months used for calculations",
            "Snowball method for debt payoff",
            "50% surplus allocated to debt, 50% to savings",
            "Weekly micro-deposits for savings goals"
        ]
        
        result = CFPSimulateOutput(
            ok=True,
            calculations=calculations,
            checksum=checksum,
            assumptions=assumptions,
            provenance_ref=f"cfp_sim_{input_data.trace_id}"
        )
        
        logger.info(f"CFP simulation completed: surplus=${monthly_surplus}, checksum={checksum[:8]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"CFP simulation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify", response_model=CFPVerifyOutput)
async def verify_calculations(input_data: CFPVerifyInput):
    """
    Verify financial calculations match expected checksum
    
    Ensures deterministic, tamper-proof calculations
    """
    try:
        # Regenerate checksum from calculations
        actual_checksum = generate_checksum(input_data.calculations)
        
        verified = actual_checksum == input_data.expected_checksum
        
        result = CFPVerifyOutput(
            ok=True,
            verified=verified,
            message="Calculations verified" if verified else "Checksum mismatch - calculations may have been tampered with"
        )
        
        logger.info(f"CFP verification: {result.message}")
        
        return result
        
    except Exception as e:
        logger.error(f"CFP verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
