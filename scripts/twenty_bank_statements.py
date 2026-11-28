import pandas as pd
import random
from datetime import datetime
import os

# Create a folder for the dummy data
os.makedirs("synthetic_data", exist_ok=True)
random.seed(42) 

# Merchants and amounts
merchants = [
    ("Whole Foods", -120, -40), ("Starbucks", -15, -5), 
    ("Amazon", -150, -15), ("Uber", -25, -10), 
    ("Tech Corp Payroll", 4000, 3500), ("Transfer to Savings", -500, -500)
]

start_date = datetime(2025, 1, 1)

# Generate 20 months of statements
for month_num in range(20):
    rows = []
    current_month = start_date.month + month_num
    current_year = start_date.year + (current_month - 1) // 12
    current_month = (current_month - 1) % 12 + 1
    
    # Add 15 random transactions per month
    for i in range(15):
        merchant, max_amt, min_amt = random.choice(merchants)
        day = random.randint(1, 28)
        date_str = f"{current_year}-{current_month:02d}-{day:02d}"
        amount = round(random.uniform(min_amt, max_amt), 2)
        
        rows.append({
            "date": date_str,
            "description": merchant,
            "amount": amount,
            "account": "Checking",
            "transaction_id": f"TX_{current_year}_{current_month:02d}_{i:03d}"
        })
        
    # Save to CSV
    df = pd.DataFrame(rows)
    filename = f"synthetic_data/statement_{current_year}_{current_month:02d}.csv"
    df.to_csv(filename, index=False)
    print(f"Generated {filename}")

print("Done! 20 synthetic bank statements generated in the 'synthetic_data' folder.")