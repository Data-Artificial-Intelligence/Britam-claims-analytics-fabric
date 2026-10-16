import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_claims_data(num_records, start_id, batch_id, start_date):
    np.random.seed(42)
    random.seed(42)
    
    claim_ids = [f"CLM-{str(i).zfill(5)}" for i in range(start_id, start_id + num_records)]
    policy_ids = [f"POL-{str(random.randint(10000, 99999))}" for _ in range(num_records)]
    
    # Generate dates within the last 2 years
    dates = [start_date - timedelta(days=random.randint(0, 730)) for _ in range(num_records)]
    date_strings = [d.strftime('%Y-%m-%d') for d in dates]
    
    # Categories (with intentional casing messiness for cleaning demo)
    categories = ['Sedan', 'SUV', 'Truck', 'Motorcycle', 'Van']
    messy_categories = [random.choice(categories) for _ in range(num_records)]
    for i in range(int(num_records * 0.05)): # 5% messy
        idx = random.randint(0, num_records - 1)
        messy_categories[idx] = messy_categories[idx].lower()
    if num_records > 100:
        messy_categories[5] = "S.U.V" # Edge case
    
    # Regions (Kenya-specific for Britam relevance)
    regions = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Nyeri']
    region_choices = [random.choice(regions) for _ in range(num_records)]
    
    # Claim amounts (Log-normal distribution to mimic real insurance skew)
    amounts = np.round(np.random.lognormal(mean=9.5, sigma=0.8, size=num_records), 2)
    
    # Status (with intentional typos for cleaning demo)
    statuses = ['Approved', 'Pending', 'Rejected', 'Under Review']
    messy_statuses = [random.choice(statuses) for _ in range(num_records)]
    for i in range(int(num_records * 0.03)): # 3% typos
        idx = random.randint(0, num_records - 1)
        if messy_statuses[idx] == 'Pending':
            messy_statuses[idx] = 'Pendng'
        elif messy_statuses[idx] == 'Approved':
            messy_statuses[idx] = 'Aproved'

    # Fraud flag (15% probability, slightly higher for certain regions/categories)
    fraud_flags = []
    for i in range(num_records):
        base_prob = 0.05
        if region_choices[i] == 'Nairobi' and messy_categories[i].upper() == 'SUV':
            base_prob = 0.15
        fraud_flags.append(1 if random.random() < base_prob else 0)
        
    # Introduce missing values in claim_amount (~5%)
    for i in range(int(num_records * 0.05)):
        idx = random.randint(0, num_records - 1)
        amounts[idx] = np.nan

    batch_ids = [batch_id] * num_records

    df = pd.DataFrame({
        'claim_id': claim_ids,
        'policy_id': policy_ids,
        'claim_date': date_strings,
        'vehicle_category': messy_categories,
        'region': region_choices,
        'claim_amount': amounts,
        'claim_status': messy_statuses,
        'is_fraud_flag': fraud_flags,
        'batch_id': batch_ids
    })
    
    return df

if __name__ == "__main__":
    print("Generating Batch 1 (1,200 records)...")
    df_batch1 = generate_claims_data(
        num_records=1200, 
        start_id=1001, 
        batch_id=1, 
        start_date=datetime(2026, 10, 17)
    )
    df_batch1.to_csv('data/claims_batch_1.csv', index=False)
    print("Saved: data/claims_batch_1.csv")

    print("Generating Batch 2 (300 records for incremental update demo)...")
    df_batch2 = generate_claims_data(
        num_records=300, 
        start_id=2201, 
        batch_id=2, 
        start_date=datetime(2026, 10, 17)
    )
    df_batch2.to_csv('data/claims_batch_2.csv', index=False)
    print("Saved: data/claims_batch_2.csv")
    
    print("\nDataset generation complete! Total records: 1,500")