"""
Bronze → Silver Transformation

Bronze data is pre-loaded below as pandas DataFrames.
Implement the transformation to produce standardized silver records.
"""

import pandas as pd
from pathlib import Path

# ==============================================================================
# TARGET SILVER SCHEMA
# ==============================================================================

SILVER_SCHEMA = {
    'patient_id': str,
    'first_name': str,
    'last_name': str,
    'date_of_birth': str,  # YYYY-MM-DD format
    'gender': str,  # M, F, or Other
    'enrollment_status': str,  # Active, Inactive, Prospect, Deceased
    'phone': str,
    'org_id': str,
}

# Example of one transformed silver record:
# {
#     'patient_id': '10001',
#     'first_name': 'Maria',
#     'last_name': 'Gonzalez',
#     'date_of_birth': '1948-03-15',
#     'gender': 'F',
#     'enrollment_status': 'Active',
#     'phone': '2175550101',
#     'org_id': 'springfield'
# }

# ==============================================================================
# BRONZE DATA (PRE-LOADED)
# ==============================================================================

DATA_DIR = Path(__file__).parent / "input_data_v2/premade_bronze_files"

# Load bronze data as DataFrames (all columns as strings)
springfield_patients = pd.read_csv(
    DATA_DIR / "bronze_springfield_patients.csv",
    dtype=str,
    keep_default_na=False
)

chicago_patients = pd.read_csv(
    DATA_DIR / "bronze_chicago_patients.csv",
    dtype=str,
    keep_default_na=False
)

print(f"Loaded {len(springfield_patients)} Springfield patients")
print(f"Loaded {len(chicago_patients)} Chicago patients")
print()
print("Springfield columns:", list(springfield_patients.columns))
print("Chicago columns:    ", list(chicago_patients.columns))
print()

# ==============================================================================
# YOUR CODE HERE
# ==============================================================================

# TODO: Implement transformation to SILVER_SCHEMA
# - Handle different column names per org (remember target schema is fixed)
# - Normalize values (gender, enrollment_status, dates)
# - Validate data quality
# - Return DataFrame(s) with SILVER_SCHEMA columns


if __name__ == "__main__":
    # Your implementation here
    pass
