import pandas as pd
import requests

BASE_URL = "http://localhost:31509"

LOGIN_URL = f"{BASE_URL}/auth/login"
CUSTOMER_URL = f"{BASE_URL}/customer"

username = input("Enter Username: ")
password = input("Enter Password: ")

login = requests.post(
    LOGIN_URL,
    json={
        "username": username,
        "password": password
    }
)

if login.status_code != 200:
    print(login.json())
    exit()

token = login.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

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

    response = requests.post(
        CUSTOMER_URL,
        json=customer,
        headers=headers
    )

    if response.status_code == 200:
        inserted += 1
    else:
        failed += 1
        print(customer["email"], response.json())

print(f"Inserted: {inserted}")
print(f"Failed: {failed}")