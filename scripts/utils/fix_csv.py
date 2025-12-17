"""
Add case_id column to the CSV file
"""
import pandas as pd

# Read the CSV
df = pd.read_csv('./camelyon16_attrimil/camelyon16_total.csv')

# Add case_id column (use slide_id as case_id since we don't have patient info)
df['case_id'] = df['slide_id']

# Reorder columns to have case_id first
df = df[['case_id', 'slide_id', 'label']]

# Save back
df.to_csv('./camelyon16_attrimil/camelyon16_total.csv', index=False)

print("Fixed CSV file - added case_id column")
print(f"Total rows: {len(df)}")
print("\nFirst few rows:")
print(df.head())
