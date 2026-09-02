import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="job_market"
)

print("MySQL Connected Successfully!")

df = pd.read_csv("cleaned_job_market_intelligence.csv")

# Convert NaN to None
df = df.astype(object).where(pd.notna(df), None)

print("CSV Loaded Successfully!")
print("Total Jobs:", len(df))

cursor = connection.cursor()

insert_query = """
INSERT INTO jobs (
    company_name,
    experience,
    salary,
    location,
    info,
    skills,
    job_url,
    min_experience,
    max_experience,
    min_salary_lpa,
    max_salary_lpa
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    values = (
        row["company_name"],
        row["Experience"],
        row["salary"],
        row["location"],
        row["info"],
        row["Skills"],
        row["Job_URL"],
        row["Min_Experience"],
        row["Max_Experience"],
        row["Min_Salary_LPA"],
        row["Max_Salary_LPA"]
    )

    cursor.execute(insert_query, values)

connection.commit()

print("All jobs inserted successfully!")

cursor.close()
connection.close()

print("MySQL connection closed.")