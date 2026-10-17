"""
Unit tests for synthetic motor claims data generation.
Validates that generated datasets meet interview requirements:
- Minimum 1,000 total records
- Required schema columns present
- Date and category columns exist
- Incremental update capability (batch_id column)
"""

import os
import sys
import pandas as pd


def test_data_files_exist():
    """Verify that the generation script produced the expected CSV files."""
    batch1_path = 'data/claims_batch_1.csv'
    batch2_path = 'data/claims_batch_2.csv'
    
    assert os.path.exists(batch1_path), f"❌ FAIL: {batch1_path} not found!"
    assert os.path.exists(batch2_path), f"❌ FAIL: {batch2_path} not found!"
    print(f"✅ PASS: Both CSV files exist.")


def test_row_counts():
    """Verify the dataset meets the interview requirement (>1,000 records total)."""
    df1 = pd.read_csv('data/claims_batch_1.csv')
    df2 = pd.read_csv('data/claims_batch_2.csv')
    
    # Check Batch 1 (Expect 1200)
    assert len(df1) == 1200, f"❌ FAIL: Expected 1200 rows in Batch 1, got {len(df1)}"
    
    # Check Batch 2 (Expect 300)
    assert len(df2) == 300, f"❌ FAIL: Expected 300 rows in Batch 2, got {len(df2)}"
    
    total_rows = len(df1) + len(df2)
    assert total_rows >= 1000, f"❌ FAIL: Total rows ({total_rows}) must be >= 1000"
    
    print(f"✅ PASS: Row counts verified (Total: {total_rows}).")


def test_schema_integrity():
    """Ensure critical columns required by the brief are present."""
    df = pd.read_csv('data/claims_batch_1.csv')
    required_cols = [
        'claim_id', 
        'policy_id', 
        'claim_date',      # At least one date column ✓
        'vehicle_category', # At least one category column ✓
        'region', 
        'claim_amount',
        'claim_status',
        'is_fraud_flag',
        'batch_id'          # For incremental updates ✓
    ]
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise AssertionError(f"❌ FAIL: Missing required columns: {missing}")
        
    print("✅ PASS: Schema integrity verified (all 9 required columns present).")


def test_incremental_update_capability():
    """Verify that batch_id exists and supports incremental loading logic."""
    df1 = pd.read_csv('data/claims_batch_1.csv')
    df2 = pd.read_csv('data/claims_batch_2.csv')
    
    # All Batch 1 records should have batch_id = 1
    assert (df1['batch_id'] == 1).all(), "❌ FAIL: Batch 1 records do not all have batch_id=1"
    
    # All Batch 2 records should have batch_id = 2
    assert (df2['batch_id'] == 2).all(), "❌ FAIL: Batch 2 records do not all have batch_id=2"
    
    # Verify no overlapping claim_ids between batches (critical for merge/upsert safety)
    overlap = set(df1['claim_id']).intersection(set(df2['claim_id']))
    assert len(overlap) == 0, f"❌ FAIL: Found {len(overlap)} duplicate claim_ids across batches!"
    
    print("✅ PASS: Incremental update capability verified (unique batch_ids, no ID overlaps).")


if __name__ == "__main__":
    try:
        test_data_files_exist()
        test_row_counts()
        test_schema_integrity()
        test_incremental_update_capability()
        print("\n🎉 ALL TESTS PASSED! Pipeline is healthy.")
        sys.exit(0)
    except AssertionError as e:
        print(e)
        sys.exit(1)