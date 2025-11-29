"""Complete legal rulesets - FDCPA, FCRA, CROA - All sections"""

COMPLETE_FDCPA_RULES = [
    # Section 803 - Definitions
    {'rule_code': 'FDCPA_803', 'rule_type': 'definitions', 'state_code': None,
     'rule_text': 'Defines debt collector, consumer, creditor, and debt.',
     'citations': {'statute': '15 U.S.C. § 1692a', 'title': 'FDCPA § 803 - Definitions'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 804 - Acquisition of location information
    {'rule_code': 'FDCPA_804', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Debt collectors acquiring location information must identify themselves but may not state they are confirming or collecting a debt.',
     'citations': {'statute': '15 U.S.C. § 1692b', 'title': 'FDCPA § 804 - Acquisition of location information'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 805 - Communication in connection with debt collection
    {'rule_code': 'FDCPA_805', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Debt collectors may not communicate with consumers at unusual times or places, at their place of employment if prohibited, or if represented by attorney.',
     'citations': {'statute': '15 U.S.C. § 1692c', 'title': 'FDCPA § 805 - Communication restrictions'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 806 - Harassment or abuse
    {'rule_code': 'FDCPA_806', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Debt collectors may not harass, oppress, or abuse any person including threats of violence, obscene language, or repeated calls.',
     'citations': {'statute': '15 U.S.C. § 1692d', 'title': 'FDCPA § 806 - Harassment or abuse'},
     'severity': 'high', 'db_version': 'v1.0'},
    
    # Section 807 - False or misleading representations
    {'rule_code': 'FDCPA_807', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Debt collectors may not use false, deceptive, or misleading representations including falsely implying they are attorneys or government representatives.',
     'citations': {'statute': '15 U.S.C. § 1692e', 'title': 'FDCPA § 807 - False or misleading representations'},
     'severity': 'high', 'db_version': 'v1.0'},
    
    # Section 808 - Unfair practices
    {'rule_code': 'FDCPA_808', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Debt collectors may not use unfair or unconscionable means including collecting amounts not authorized by agreement or law.',
     'citations': {'statute': '15 U.S.C. § 1692f', 'title': 'FDCPA § 808 - Unfair practices'},
     'severity': 'high', 'db_version': 'v1.0'},
    
    # Section 809 - Validation of debts
    {'rule_code': 'FDCPA_809', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Within five days after initial communication, debt collector must send written notice containing debt amount, creditor name, and validation rights. Consumer has 30 days to dispute.',
     'citations': {'statute': '15 U.S.C. § 1692g', 'title': 'FDCPA § 809 - Validation of debts'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 810 - Multiple debts
    {'rule_code': 'FDCPA_810', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'If consumer owes multiple debts and makes payment, collector must apply payment as consumer directs.',
     'citations': {'statute': '15 U.S.C. § 1692h', 'title': 'FDCPA § 810 - Multiple debts'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 811 - Legal actions by debt collectors
    {'rule_code': 'FDCPA_811', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Legal actions must be brought in judicial district where consumer resides or where contract was signed.',
     'citations': {'statute': '15 U.S.C. § 1692i', 'title': 'FDCPA § 811 - Legal actions'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 812 - Furnishing deceptive forms
    {'rule_code': 'FDCPA_812', 'rule_type': 'debt_collection', 'state_code': None,
     'rule_text': 'Debt collectors may not design, compile, or furnish any form that creates false belief about its source or legal status.',
     'citations': {'statute': '15 U.S.C. § 1692j', 'title': 'FDCPA § 812 - Furnishing deceptive forms'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 813 - Civil liability
    {'rule_code': 'FDCPA_813', 'rule_type': 'liability', 'state_code': None,
     'rule_text': 'Debt collectors who violate FDCPA are liable for actual damages, statutory damages up to $1,000, and attorney fees.',
     'citations': {'statute': '15 U.S.C. § 1692k', 'title': 'FDCPA § 813 - Civil liability'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 814 - Administrative enforcement
    {'rule_code': 'FDCPA_814', 'rule_type': 'enforcement', 'state_code': None,
     'rule_text': 'FTC has primary enforcement authority for FDCPA violations.',
     'citations': {'statute': '15 U.S.C. § 1692l', 'title': 'FDCPA § 814 - Administrative enforcement'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 815 - Reports to Congress
    {'rule_code': 'FDCPA_815', 'rule_type': 'reporting', 'state_code': None,
     'rule_text': 'FTC must report to Congress on debt collection practices.',
     'citations': {'statute': '15 U.S.C. § 1692m', 'title': 'FDCPA § 815 - Reports to Congress'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 816 - Relation to state laws
    {'rule_code': 'FDCPA_816', 'rule_type': 'jurisdiction', 'state_code': None,
     'rule_text': 'FDCPA does not preempt state laws providing greater consumer protection.',
     'citations': {'statute': '15 U.S.C. § 1692n', 'title': 'FDCPA § 816 - Relation to state laws'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 817 - Exemption for state regulation
    {'rule_code': 'FDCPA_817', 'rule_type': 'exemption', 'state_code': None,
     'rule_text': 'FTC may exempt debt collectors if state law provides substantially similar protections.',
     'citations': {'statute': '15 U.S.C. § 1692o', 'title': 'FDCPA § 817 - Exemption for state regulation'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 818 - Effective date
    {'rule_code': 'FDCPA_818', 'rule_type': 'administrative', 'state_code': None,
     'rule_text': 'FDCPA took effect on September 20, 1977.',
     'citations': {'statute': '15 U.S.C. § 1692 note', 'title': 'FDCPA § 818 - Effective date'},
     'severity': 'low', 'db_version': 'v1.0'},
]

COMPLETE_FCRA_RULES = [
    # Section 604 - Permissible purposes
    {'rule_code': 'FCRA_604', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Credit reports may only be furnished for permissible purposes including credit transactions, employment, insurance underwriting, or with consumer consent.',
     'citations': {'statute': '15 U.S.C. § 1681b', 'title': 'FCRA § 604 - Permissible purposes'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 605 - Requirements for adverse information
    {'rule_code': 'FCRA_605', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Most negative information must be removed after 7 years. Bankruptcies after 10 years. Unpaid judgments after 7 years or until statute of limitations expires.',
     'citations': {'statute': '15 U.S.C. § 1681c', 'title': 'FCRA § 605 - Requirements relating to information contained in consumer reports'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 606 - Disclosure requirements
    {'rule_code': 'FCRA_606', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Credit bureaus must make all information in consumer files available to the consumer.',
     'citations': {'statute': '15 U.S.C. § 1681d', 'title': 'FCRA § 606 - Disclosure requirements'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 607 - Compliance procedures
    {'rule_code': 'FCRA_607', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Credit bureaus must follow reasonable procedures to assure maximum possible accuracy of consumer reports.',
     'citations': {'statute': '15 U.S.C. § 1681e', 'title': 'FCRA § 607 - Compliance procedures'},
     'severity': 'high', 'db_version': 'v1.0'},
    
    # Section 609 - Disclosures to consumers
    {'rule_code': 'FCRA_609', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Consumers have right to obtain all information in their file, sources of information, and recipients of reports.',
     'citations': {'statute': '15 U.S.C. § 1681g', 'title': 'FCRA § 609 - Disclosures to consumers'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 611 - Procedure for disputed information
    {'rule_code': 'FCRA_611', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Credit bureaus must investigate consumer disputes within 30 days and correct or delete inaccurate information. Must notify consumer of results.',
     'citations': {'statute': '15 U.S.C. § 1681i', 'title': 'FCRA § 611 - Procedure for correcting incomplete or inaccurate information'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 615 - Requirements on users of consumer reports
    {'rule_code': 'FCRA_615', 'rule_type': 'credit_reporting', 'state_code': None,
     'rule_text': 'Users of credit reports must provide adverse action notices if they take negative action based on credit report.',
     'citations': {'statute': '15 U.S.C. § 1681m', 'title': 'FCRA § 615 - Requirements on users of consumer reports'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 616 - Civil liability for willful noncompliance
    {'rule_code': 'FCRA_616', 'rule_type': 'liability', 'state_code': None,
     'rule_text': 'Willful violations subject to actual damages or statutory damages $100-$1,000, plus punitive damages and attorney fees.',
     'citations': {'statute': '15 U.S.C. § 1681n', 'title': 'FCRA § 616 - Civil liability for willful noncompliance'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 617 - Civil liability for negligent noncompliance
    {'rule_code': 'FCRA_617', 'rule_type': 'liability', 'state_code': None,
     'rule_text': 'Negligent violations subject to actual damages and attorney fees.',
     'citations': {'statute': '15 U.S.C. § 1681o', 'title': 'FCRA § 617 - Civil liability for negligent noncompliance'},
     'severity': 'low', 'db_version': 'v1.0'},
]

COMPLETE_CROA_RULES = [
    # Section 403 - Prohibited practices
    {'rule_code': 'CROA_403', 'rule_type': 'credit_repair', 'state_code': None,
     'rule_text': 'Credit repair organizations may not make untrue or misleading statements, advise consumers to make false statements, or charge fees before services are fully performed.',
     'citations': {'statute': '15 U.S.C. § 1679b', 'title': 'CROA § 403 - Prohibited practices'},
     'severity': 'high', 'db_version': 'v1.0'},
    
    # Section 404 - Required contract disclosures
    {'rule_code': 'CROA_404', 'rule_type': 'credit_repair', 'state_code': None,
     'rule_text': 'Credit repair contracts must include specific disclosures about services, costs, and consumer rights in writing.',
     'citations': {'statute': '15 U.S.C. § 1679c', 'title': 'CROA § 404 - Required disclosures'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 405 - Right to cancel
    {'rule_code': 'CROA_405', 'rule_type': 'credit_repair', 'state_code': None,
     'rule_text': 'Consumers have right to cancel credit repair contract within 3 business days without penalty.',
     'citations': {'statute': '15 U.S.C. § 1679d', 'title': 'CROA § 405 - Right to cancel'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 406 - Noncompliance with contract
    {'rule_code': 'CROA_406', 'rule_type': 'credit_repair', 'state_code': None,
     'rule_text': 'Contracts not meeting CROA requirements are void and unenforceable.',
     'citations': {'statute': '15 U.S.C. § 1679e', 'title': 'CROA § 406 - Noncompliance'},
     'severity': 'medium', 'db_version': 'v1.0'},
    
    # Section 407 - Civil liability
    {'rule_code': 'CROA_407', 'rule_type': 'liability', 'state_code': None,
     'rule_text': 'Violations subject to actual damages, punitive damages, and attorney fees.',
     'citations': {'statute': '15 U.S.C. § 1679g', 'title': 'CROA § 407 - Civil liability'},
     'severity': 'low', 'db_version': 'v1.0'},
    
    # Section 408 - Administrative enforcement
    {'rule_code': 'CROA_408', 'rule_type': 'enforcement', 'state_code': None,
     'rule_text': 'FTC enforces CROA compliance.',
     'citations': {'statute': '15 U.S.C. § 1679h', 'title': 'CROA § 408 - Administrative enforcement'},
     'severity': 'low', 'db_version': 'v1.0'},
]

async def seed_complete_legal_rules(db):
    """Seed complete FDCPA, FCRA, CROA rulesets into MongoDB"""
    all_rules = COMPLETE_FDCPA_RULES + COMPLETE_FCRA_RULES + COMPLETE_CROA_RULES
    
    for rule in all_rules:
        await db.legal_rules.update_one(
            {'rule_code': rule['rule_code']},
            {'$set': rule},
            upsert=True
        )
    
    return len(all_rules)
