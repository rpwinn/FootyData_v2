# Verification Scripts

This directory contains verification scripts that compare data stored in our staging tables against fresh API calls to ensure data integrity and completeness.

## Purpose

Each verification script:
1. Makes a fresh API call to get current data
2. Retrieves stored data from the corresponding staging table
3. Compares them field-by-field to ensure exact matching
4. Reports any discrepancies found

## Usage

```bash
# Verify countries data
python3 src/verification/verify_countries_data_comparison.py

# Future verification scripts will follow the same pattern:
# python3 src/verification/verify_[endpoint]_data_comparison.py
```

## Scripts

- `verify_countries_data_comparison.py` - Verifies countries staging table data against `/countries` API endpoint

## Verification Pattern

Each verification script should:
- ✅ Compare fresh API response with stored database data
- ✅ Check all required fields match exactly
- ✅ Verify raw_data contains correct individual records
- ✅ Report detailed mismatches if any found
- ✅ Provide summary statistics

This ensures our ETL processes are working correctly and data integrity is maintained. 