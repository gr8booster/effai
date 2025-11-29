"""Seed initial data for PostgreSQL database"""
import asyncio
import asyncpg
import os
import json
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


async def seed_statute_of_limitations():
    """Seed state-specific statute of limitations data"""
    dsn = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    
    conn = await asyncpg.connect(dsn)
    
    # Sample SOL data for major states
    sol_data = [
        ('AL', 'credit_card', 3),
        ('AL', 'written_contract', 6),
        ('CA', 'credit_card', 4),
        ('CA', 'written_contract', 4),
        ('FL', 'credit_card', 4),
        ('FL', 'written_contract', 5),
        ('IL', 'credit_card', 5),
        ('IL', 'written_contract', 10),
        ('NY', 'credit_card', 6),
        ('NY', 'written_contract', 6),
        ('OH', 'credit_card', 6),
        ('OH', 'written_contract', 8),
        ('TX', 'credit_card', 4),
        ('TX', 'written_contract', 4),
        ('PA', 'credit_card', 4),
        ('PA', 'written_contract', 4),
        ('GA', 'credit_card', 4),
        ('GA', 'written_contract', 6),
        ('NC', 'credit_card', 3),
        ('NC', 'written_contract', 3),
        ('MI', 'credit_card', 6),
        ('MI', 'written_contract', 6),
    ]
    
    for state, debt_type, years in sol_data:
        try:
            await conn.execute("""
                INSERT INTO statute_of_limitations (state_code, debt_type, years, notes)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (state_code, debt_type) DO NOTHING
            """, state, debt_type, years, f"Statute of limitations for {debt_type} in {state}")
            print(f"Inserted SOL: {state} - {debt_type} - {years} years")
        except Exception as e:
            print(f"Error inserting {state}/{debt_type}: {e}")
    
    await conn.close()
    print("Statute of limitations data seeded successfully")


async def seed_legal_rules():
    """Seed basic legal rules"""
    dsn = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    
    conn = await asyncpg.connect(dsn)
    
    rules = [
        {
            'rule_code': 'FDCPA_809',
            'rule_type': 'debt_collection',
            'state_code': None,
            'rule_text': 'A debt collector must provide verification of the debt if requested by the consumer within 30 days.',
            'citations': {'statute': '15 U.S.C. § 1692g', 'title': 'FDCPA § 809 - Validation of debts'},
            'severity': 'low',
            'db_version': 'v1.0'
        },
        {
            'rule_code': 'FCRA_611',
            'rule_type': 'credit_reporting',
            'state_code': None,
            'rule_text': 'Credit bureaus must investigate disputes within 30 days and correct or delete inaccurate information.',
            'citations': {'statute': '15 U.S.C. § 1681i', 'title': 'FCRA § 611 - Procedure for correcting incomplete or inaccurate information'},
            'severity': 'low',
            'db_version': 'v1.0'
        },
        {
            'rule_code': 'FDCPA_805',
            'rule_type': 'debt_collection',
            'state_code': None,
            'rule_text': 'A debt collector may not communicate with a consumer if the consumer notifies the collector in writing to cease communication.',
            'citations': {'statute': '15 U.S.C. § 1692c', 'title': 'FDCPA § 805 - Communication in connection with debt collection'},
            'severity': 'low',
            'db_version': 'v1.0'
        }
    ]
    
    for rule in rules:
        try:
            await conn.execute("""
                INSERT INTO legal_rules (rule_code, rule_type, state_code, rule_text, citations, severity, db_version)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7)
                ON CONFLICT (rule_code) DO NOTHING
            """, rule['rule_code'], rule['rule_type'], rule['state_code'], rule['rule_text'],
                rule['citations'], rule['severity'], rule['db_version'])
            print(f"Inserted legal rule: {rule['rule_code']}")
        except Exception as e:
            print(f"Error inserting rule {rule['rule_code']}: {e}")
    
    await conn.close()
    print("Legal rules seeded successfully")


async def main():
    print("Starting database seeding...")
    await seed_statute_of_limitations()
    await seed_legal_rules()
    print("All seed data loaded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
