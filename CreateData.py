import pandas as pd
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import numpy as np
import json

# Initialize Faker to generate fake text data
fake = Faker()

# List of pre-defined ICD-10 diagnostic codes
columns = ["ICD10CM", "Description"]
colspecs = [(0, 7), (8, None)]
icd10_codes = pd.read_fwf("icd10cm-codes-2024.txt",colspecs=colspecs, header=None,  names=columns, index_col=False)

# List of pre-defined HCPC procedure codes
CPT_codes = pd.read_csv("2022_DHS_Code_List_Addendum_10_28_21/CPT_codes.csv")
CPT_codes.head()
CPTcode_dict = CPT_codes.set_index('CPT_code')['Description'].to_dict()

race_ethnicity = ["Non Hispanic White", "Hispanic White", "Non Hispanic White", "Non Hispanic Black", "Asian American and Pacific Islanders", "Others"]
# Initialize the dataset
dataset = []

# Generate 10,000 records
for i in range(10000):
    record = {
        "id": str(random.randint(10000000, 99999999)),  # 8-digit ID number
        "age": random.randint(1,80),
        "gender": str(random.randint(0,1)),
        "race": random.choice(race_ethnicity),
        "patient_id": str(random.randint(100000, 999999)),  # 6-digit patient ID
        "datetime": (datetime(2016, 1, 1) + timedelta(days=random.randint(0, 2191), seconds=random.randint(0, 86399))).strftime("%Y-%m-%d %H:%M:%S"),
        "hospital_id": random.randint(100, 999),  # 3-digit hospital ID
        "doctor_id": random.randint(1000, 9999),  # 4-digit doctor ID
        "diagnostics": {f"diagnostic_{j}": random.choice(icd10_codes['ICD10CM']) for j in range(1, 11)},
        "procedures": {f"procedure_{j}": random.choice(CPT_codes['CPT_code']) for j in range(1, 11)},
        "complaint_description": fake.text(),  # Fake text data
        "length_of_stay": random.randint(1, 30),  # Length of stay between 1 and 30 hours
        "discharge_note": fake.sentence(),  # Fake sentence for discharge note
        "cost": round(random.uniform(100.0, 5000.0), 2),  # Random cost between $100 and $5000
        "patient_rating": round(random.uniform(1.0, 5.0), 1)  # Random patient rating between 1.0 and 5.0
    }
    dataset.append(record)


json_object = json.dumps(dataset)

with open('dataset.json', "w") as outfile:
    outfile.write(json_object)