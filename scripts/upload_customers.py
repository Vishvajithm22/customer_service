import pandas as pd
import requests

URL = "http://localhost:31509/customer"

df = pd.read_excel("customers.xlsx")

inserted = 0
failed = 0

for _, row in df.iterrows():

    customer = {
        "name": row["name"],
        "company": row["company"],
        "email": row["email"],
        "phone": str(row["phone"]),
        "yearly_sale": float(row["yearly_sale"]),
        "sector": row["sector"]
    }

    response = requests.post(URL, json=customer)

    if response.status_code == 200:
        inserted += 1
    else:
        failed += 1
        print(customer["email"], response.json())

print(f"Inserted: {inserted}")
print(f"Failed: {failed}")