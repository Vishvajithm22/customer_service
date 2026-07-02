from faker import Faker
import pandas as pd
import random

fake = Faker()

SECTORS = [
    "IT",
    "Banking",
    "Healthcare",
    "Manufacturing",
    "Retail"
]

COMPANIES = [
    "Google",
    "Microsoft",
    "Amazon",
    "Apple",
    "Tesla",
    "IBM",
    "Oracle",
    "Intel",
    "Cisco",
    "Samsung",
    "Adobe",
    "Dell",
    "Accenture",
    "Infosys",
    "TCS"
]

customers = []

emails = set()

for _ in range(1000):

    while True:
        first = fake.first_name()
        last = fake.last_name()

        company = random.choice(COMPANIES)

        email = (
            f"{first.lower()}."
            f"{last.lower()}@"
            f"{company.lower()}.com"
        )

        if email not in emails:
            emails.add(email)
            break

    customer = {
        "name": f"{first} {last}",
        "company": company,
        "email": email,
        "phone": str(random.randint(6000000000, 9999999999)),
        "yearly_sale": random.randint(
            1_000_000,
            150_000_000
        ),
        "sector": random.choice(SECTORS)
    }

    customers.append(customer)

df = pd.DataFrame(customers)

df.to_excel(
    "customers.xlsx",
    index=False
)

print("1000 customers generated successfully.")