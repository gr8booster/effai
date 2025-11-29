"""
Complete Micro-Learning Library - 50+ Production Lessons
Categories: Savings, Debt, Credit, Legal, Budgeting
"""

COMPLETE_LESSONS = {
    # SAVINGS (10 lessons)
    "emergency_fund_101": {"title": "Emergency Fund 101", "category": "savings", "duration_min": 5, "html": "<h2>Why $1000 First</h2><p>Covers 80% of emergencies. Start now.</p>"},
    "savings_automation": {"title": "Automate Your Savings", "category": "savings", "duration_min": 4, "html": "<h2>Set It & Forget It</h2><p>Direct deposit split. Round-ups. Scheduled transfers.</p>"},
    "50_30_20_rule": {"title": "50/30/20 Budget", "category": "savings", "duration_min": 5, "html": "<h2>Simple Budget</h2><p>50% needs, 30% wants, 20% savings.</p>"},
    "high_yield_savings": {"title": "High-Yield Savings Accounts", "category": "savings", "duration_min": 6, "html": "<h2>Maximize Interest</h2><p>Online banks offer 4-5% APY vs 0.01% at big banks.</p>"},
    "cash_stuffing": {"title": "Cash Envelope System", "category": "savings", "duration_min": 4, "html": "<h2>Physical Budget Control</h2><p>Allocate cash to envelopes. When it's gone, stop spending.</p>"},
    "sinking_funds": {"title": "Sinking Funds Strategy", "category": "savings", "duration_min": 6, "html": "<h2>Plan for Big Expenses</h2><p>Save monthly for annual costs: insurance, holidays, car maintenance.</p>"},
    "zero_based_budget": {"title": "Zero-Based Budgeting", "category": "savings", "duration_min": 7, "html": "<h2>Every Dollar Has a Job</h2><p>Income - expenses - savings = $0. No money unassigned.</p>"},
    "bi_weekly_savings": {"title": "Bi-Weekly Savings Hack", "category": "savings", "duration_min": 4, "html": "<h2>26 Paychecks = 2 Extra</h2><p>Paid bi-weekly? Save those 2 extra checks yearly.</p>"},
    "no_spend_challenge": {"title": "30-Day No-Spend Challenge", "category": "savings", "duration_min": 5, "html": "<h2>Reset Spending Habits</h2><p>One month: buy only essentials. Bank the difference.</p>"},
    "savings_milestones": {"title": "Savings Milestones", "category": "savings", "duration_min": 4, "html": "<h2>$1K → $5K → $10K</h2><p>Celebrate each goal. Track progress visually.</p>"},
    
    # DEBT (15 lessons)
    "debt_validation_rights": {"title": "FDCPA Validation Rights", "category": "debt", "duration_min": 6, "html": "<h2>Your Legal Shield</h2><p>Request validation within 30 days. They must prove it or stop.</p>"},
    "statute_of_limitations": {"title": "Time-Barred Debts", "category": "debt", "duration_min": 7, "html": "<h2>Old Debts Can't Sue</h2><p>Each state: 3-10 years. After that, unenforceable.</p>"},
    "debt_snowball": {"title": "Debt Snowball Method", "category": "debt", "duration_min": 6, "html": "<h2>Smallest Balance First</h2><p>Quick wins = motivation. Pay minimums on all, extra on smallest.</p>"},
    "debt_avalanche": {"title": "Debt Avalanche Method", "category": "debt", "duration_min": 6, "html": "<h2>Highest Interest First</h2><p>Save most money. Pay minimums on all, extra on highest APR.</p>"},
    "cease_and_desist": {"title": "Cease Communication Rights", "category": "debt", "duration_min": 5, "html": "<h2>Stop The Calls</h2><p>Written request = they must stop contact except to confirm or notify of legal action.</p>"},
    "settlement_negotiation": {"title": "Debt Settlement Tactics", "category": "debt", "duration_min": 8, "html": "<h2>40-60% Settlements</h2><p>Old debts, charged-off. Start at 25%, get it in writing first.</p>"},
    "pay_for_delete": {"title": "Pay-for-Delete Strategy", "category": "debt", "duration_min": 7, "html": "<h2>Remove From Credit</h2><p>Offer payment IF they delete tradeline. Not all agree, but many do.</p>"},
    "dealing_with_collectors": {"title": "Talking to Collectors", "category": "debt", "duration_min": 5, "html": "<h2>Stay in Control</h2><p>Request written validation. Never admit debt. Never give bank access.</p>"},
    "wage_garnishment": {"title": "Stopping Garnishment", "category": "debt", "duration_min": 6, "html": "<h2>Your Options</h2><p>Exemptions, negotiate, contest, bankruptcy. Act before it starts.</p>"},
    "medical_debt_rules": {"title": "Medical Debt Special Rules", "category": "debt", "duration_min": 5, "html": "<h2>180-Day Protection</h2><p>Paid medical collections removed. Under $500 not reported.</p>"},
    "student_loan_defense": {"title": "Student Loan Rights", "category": "debt", "duration_min": 7, "html": "<h2>Federal Protections</h2><p>Income-driven repayment. Forgiveness programs. Rehabilitation.</p>"},
    "bankruptcy_chapter7": {"title": "Chapter 7 Bankruptcy", "category": "debt", "duration_min": 8, "html": "<h2>Fresh Start</h2><p>Wipes most debt in 3-4 months. Costs $1000-2000. Stays on report 10 years.</p>"},
    "bankruptcy_chapter13": {"title": "Chapter 13 Bankruptcy", "category": "debt", "duration_min": 8, "html": "<h2>Repayment Plan</h2><p>3-5 year plan. Keep assets. Lower payments. Stops foreclosure.</p>"},
    "debt_consolidation": {"title": "Debt Consolidation Pros/Cons", "category": "debt", "duration_min": 6, "html": "<h2>One Payment</h2><p>Pro: Simplicity. Con: May cost more long-term. Read fine print.</p>"},
    "collection_lawsuit_response": {"title": "Responding to Collection Lawsuit", "category": "debt", "duration_min": 9, "html": "<h2>Don't Ignore</h2><p>Answer in 20-30 days. Demand proof. Consider attorney. Default = they win.</p>"},
    
    # CREDIT (15 lessons)
    "credit_score_factors": {"title": "5 Credit Score Factors", "category": "credit", "duration_min": 7, "html": "<h2>What Matters</h2><p>35% payment, 30% utilization, 15% age, 10% mix, 10% new.</p>"},
    "credit_utilization": {"title": "30% Utilization Rule", "category": "credit", "duration_min": 5, "html": "<h2>Keep Below 30%</h2><p>High balances = 30% of score. Pay down highest utilization first.</p>"},
    "building_credit_scratch": {"title": "Building Credit From Zero", "category": "credit", "duration_min": 6, "html": "<h2>Secured Card Path</h2><p>$200-500 deposit. Small purchases. Pay full. 12-18 months to good score.</p>"},
    "authorized_user_boost": {"title": "Authorized User Strategy", "category": "credit", "duration_min": 5, "html": "<h2>Piggybacking</h2><p>Added to old, good account. Can add 50-100 points in 60 days.</p>"},
    "credit_report_errors": {"title": "Common Report Errors", "category": "credit", "duration_min": 6, "html": "<h2>What to Look For</h2><p>Wrong accounts. Duplicate entries. Incorrect balances. Old info >7 years.</p>"},
    "disputing_bureaus": {"title": "Filing Credit Disputes", "category": "credit", "duration_min": 8, "html": "<h2>30-Day Investigation</h2><p>Letter to bureau. They must verify or delete. Certified mail.</p>"},
    "goodwill_letters": {"title": "Goodwill Adjustment Letters", "category": "credit", "duration_min": 5, "html": "<h2>Asking Forgiveness</h2><p>One late payment? Good history otherwise? Politely request removal.</p>"},
    "hard_soft_inquiries": {"title": "Credit Inquiries Explained", "category": "credit", "duration_min": 4, "html": "<h2>Hard vs Soft</h2><p>Soft = no impact (checking your own). Hard = -5 to -10 points (applications).</p>"},
    "credit_age_strategy": {"title": "Credit Age Optimization", "category": "credit", "duration_min": 5, "html": "<h2>Keep Old Accounts Open</h2><p>Average age matters. Don't close oldest card even if unused.</p>"},
    "credit_mix_guide": {"title": "Credit Mix Matters", "category": "credit", "duration_min": 5, "html": "<h2>Variety = 10% of Score</h2><p>Cards + installment loan + mortgage = better mix. Don't take debt just for this.</p>"},
    "rapid_rescore": {"title": "Rapid Rescore Process", "category": "credit", "duration_min": 6, "html": "<h2>72-Hour Updates</h2><p>Mortgage lender tool. Pay down balances, update fast. Not available to consumers directly.</p>"},
    "credit_freeze_guide": {"title": "Credit Freeze vs Lock", "category": "credit", "duration_min": 6, "html": "<h2>Identity Protection</h2><p>Freeze = free, secure. Lock = paid, instant. Both prevent new accounts.</p>"},
    "charge_off_explained": {"title": "Charge-Offs Demystified", "category": "credit", "duration_min": 7, "html": "<h2>Not Forgiven</h2><p>Charged-off doesn't mean you don't owe. Still collectible. Still hurts score.</p>"},
    "credit_repair_scams": {"title": "Avoiding Credit Repair Scams", "category": "credit", "duration_min": 6, "html": "<h2>Red Flags</h2><p>Pay upfront? Guarantee score increase? Create new identity? = SCAM. You can DIY for free.</p>"},
    "payment_history_recovery": {"title": "Rebuilding Payment History", "category": "credit", "duration_min": 6, "html": "<h2>35% of Your Score</h2><p>One late? Set up autopay. Multiple? 24 months on-time payments heal it.</p>"},
    
    # LEGAL (10 lessons)
    "fdcpa_overview": {"title": "FDCPA Overview", "category": "legal", "duration_min": 8, "html": "<h2>Federal Protection</h2><p>15 U.S.C. § 1692. Limits what collectors can do. Know your rights.</p>"},
    "fcra_overview": {"title": "FCRA Overview", "category": "legal", "duration_min": 8, "html": "<h2>Credit Reporting Law</h2><p>15 U.S.C. § 1681. Bureaus must investigate disputes. 30 days.</p>"},
    "croa_overview": {"title": "CROA - Credit Repair Law", "category": "legal", "duration_min": 7, "html": "<h2>Protection from Scams</h2><p>15 U.S.C. § 1679. Credit repair orgs can't charge upfront or lie.</p>"},
    "consumer_rights_summary": {"title": "Your Consumer Rights Summary", "category": "legal", "duration_min": 6, "html": "<h2>Know Your Protections</h2><p>Validation. Cease contact. Dispute. Sue for violations. Get damages.</p>"},
    "legal_timelines": {"title": "Important Legal Deadlines", "category": "legal", "duration_min": 6, "html": "<h2>Time-Sensitive</h2><p>30 days: validation request. 20-30 days: lawsuit answer. 7 years: most negatives.</p>"},
    "suing_collectors": {"title": "When to Sue a Collector", "category": "legal", "duration_min": 7, "html": "<h2>FDCPA Violations</h2><p>Harassment? False threats? You can sue. Up to $1000 + actual damages + attorney fees.</p>"},
    "fcra_violations": {"title": "Common FCRA Violations", "category": "legal", "duration_min": 6, "html": "<h2>Bureau Failures</h2><p>Didn't investigate? Re-inserted deleted info? You can sue.</p>"},
    "debt_validation_process": {"title": "Debt Validation Process", "category": "legal", "duration_min": 8, "html": "<h2>How It Works</h2><p>You request. They provide proof. No proof = must stop collection.</p>"},
    "identity_theft_debt": {"title": "Disputing Fraudulent Debt", "category": "legal", "duration_min": 7, "html": "<h2>Not Your Debt</h2><p>Police report. FTC affidavit. Creditor must investigate. Not your responsibility.</p>"},
    "garnishment_exemptions": {"title": "Wage Garnishment Exemptions", "category": "legal", "duration_min": 7, "html": "<h2>Protected Income</h2><p>SSI, disability, unemployment often exempt. File exemption claim immediately.</p>"},
    
    # BUDGETING (10 lessons)
    "tracking_expenses": {"title": "Tracking Every Dollar", "category": "budgeting", "duration_min": 5, "html": "<h2>Awareness = Control</h2><p>Track 30 days. See patterns. Cut unconscious spending.</p>"},
    "envelope_budgeting": {"title": "Digital Envelope Method", "category": "budgeting", "duration_min": 5, "html": "<h2>Category Buckets</h2><p>Assign every dollar to category. Stop when category empty.</p>"},
    "cutting_subscriptions": {"title": "Subscription Audit", "category": "budgeting", "duration_min": 4, "html": "<h2>$10/mo = $120/year</h2><p>Cancel unused streaming, gym, apps. Save $50-200/month.</p>"},
    "negotiating_bills": {"title": "Negotiating Monthly Bills", "category": "budgeting", "duration_min": 6, "html": "<h2>Just Ask</h2><p>Cable, internet, insurance. Call and ask for better rate. Works 60% of time.</p>"},
    "meal_planning_savings": {"title": "Meal Planning = $300/mo Savings", "category": "budgeting", "duration_min": 6, "html": "<h2>Stop Eating Out</h2><p>Plan weekly meals. Grocery shop once. Save $200-400/month.</p>"},
    "utility_reduction": {"title": "Cutting Utility Costs", "category": "budgeting", "duration_min": 5, "html": "<h2>Simple Wins</h2><p>LED bulbs. Programmable thermostat. Unplug devices. Save $30-80/month.</p>"},
    "insurance_optimization": {"title": "Optimizing Insurance Costs", "category": "budgeting", "duration_min": 7, "html": "<h2>Shop Annually</h2><p>Bundle home+auto. Raise deductibles. Save $500-1500/year.</p>"},
    "side_hustle_ideas": {"title": "Quick Side Income", "category": "budgeting", "duration_min": 6, "html": "<h2>Extra $500/mo</h2><p>Freelance, gig apps, sell items. Even $200/mo = $2400/year.</p>"},
    "tax_optimization": {"title": "Maximizing Tax Refunds", "category": "budgeting", "duration_min": 7, "html": "<h2>Common Deductions</h2><p>Student loan interest. Medical over 7.5% AGI. Charity. Don't leave money behind.</p>"},
    "financial_goals_setting": {"title": "SMART Financial Goals", "category": "budgeting", "duration_min": 6, "html": "<h2>Specific, Measurable</h2><p>Not 'save more'. Instead: 'Save $1000 in 5 months = $50/week'.</p>"},
    
    # ADVANCED (10 lessons)
    "credit_card_rewards": {"title": "Maximizing Credit Card Rewards", "category": "advanced", "duration_min": 7, "html": "<h2>Cash Back Strategy</h2><p>Only if paying full. 2% on everything or 5% categories. = $300-500/year free money.</p>"},
    "investment_basics": {"title": "Investing After Emergency Fund", "category": "advanced", "duration_min": 8, "html": "<h2>After You're Stable</h2><p>401k match first. Then Roth IRA. Then taxable. Index funds > individual stocks.</p>"},
    "compound_interest": {"title": "Compound Interest Explained", "category": "advanced", "duration_min": 6, "html": "<h2>Money Makes Money</h2><p>$100/mo at 7% = $121K in 30 years. Start young. Time > timing.</p>"},
    "retirement_milestones": {"title": "Retirement Savings by Age", "category": "advanced", "duration_min": 7, "html": "<h2>Age-Based Targets</h2><p>30: 1x salary. 40: 3x. 50: 6x. 60: 8x. 67: 10x.</p>"},
    "hsa_triple_advantage": {"title": "HSA Triple Tax Advantage", "category": "advanced", "duration_min": 6, "html": "<h2>Better Than 401k</h2><p>Tax deductible going in. Grows tax-free. Withdrawals tax-free for medical.</p>"},
    "real_estate_basics": {"title": "First Home Buying 101", "category": "advanced", "duration_min": 9, "html": "<h2>20% Down Myth</h2><p>FHA = 3.5% down. Save closing costs + moving. Budget for maintenance.</p>"},
    "estate_planning_basics": {"title": "Basic Estate Planning", "category": "advanced", "duration_min": 8, "html": "<h2>Protect Your Family</h2><p>Will. Beneficiaries. Power of attorney. Healthcare directive. Do it now.</p>"},
    "insurance_needs": {"title": "Insurance You Actually Need", "category": "advanced", "duration_min": 7, "html": "<h2>Term Life, Health, Disability</h2><p>Skip extended warranties. Get term life if dependents. Disability = underrated.</p>"},
    "financial_advisor_guide": {"title": "Do You Need a Financial Advisor?", "category": "advanced", "duration_min": 7, "html": "<h2>Fee-Only vs Commission</h2><p>DIY if simple. Complex estate? Find fiduciary fee-only advisor.</p>"},
    "teaching_kids_money": {"title": "Teaching Kids About Money", "category": "advanced", "duration_min": 6, "html": "<h2>Start Early</h2><p>Allowance. Savings jar. Let them make small mistakes. Financial literacy = life skill.</p>"},
}

# Total: 50 lessons exactly
print(f"Complete library: {len(COMPLETE_LESSONS)} lessons")
