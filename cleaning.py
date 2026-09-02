import pandas as pd

df = pd.read_csv("job_market_intelligence.csv")

# Remove unwanted index column
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

print("Before Cleaning:")
print(df.head())
print("Total Rows:", len(df))

# Clean Company Names
df["company_name"] = df["company_name"].str.replace(
    r"\d.*?Reviews",
    "",
    regex=True
).str.strip()

print("\nCleaned Company Names:")
print(df["company_name"].head())


# Clean Experience
df["Experience"] = df["Experience"].replace("Missing", "")

experience = df["Experience"].str.extract(
    r"(\d+)\s*-\s*(\d+)"
)

df["Min_Experience"] = experience[0]
df["Max_Experience"] = experience[1]

# Handle values like "0 Yrs"
single_experience = df["Experience"].str.extract(
    r"^(\d+)\s*Yrs$"
)

df["Min_Experience"] = df["Min_Experience"].fillna(single_experience[0])
df["Max_Experience"] = df["Max_Experience"].fillna(single_experience[0])

# Convert to numeric
df["Min_Experience"] = pd.to_numeric(
    df["Min_Experience"],
    errors="coerce"
)

df["Max_Experience"] = pd.to_numeric(
    df["Max_Experience"],
    errors="coerce"
)

print("\nExperience After Cleaning:")
print(
    df[
        ["Experience", "Min_Experience", "Max_Experience"]
    ].head(10)
)

# Clean Salary
df["salary"] = df["salary"].fillna("")

# Extract salary range
salary_range = df["salary"].str.extract(
    r"([\d,.]+)\s*-\s*([\d,.]+)\s*Lacs?"
)

df["Min_Salary_LPA"] = pd.to_numeric(
    salary_range[0].str.replace(",", ""),
    errors="coerce"
)

df["Max_Salary_LPA"] = pd.to_numeric(
    salary_range[1].str.replace(",", ""),
    errors="coerce"
)

# Handle salary values where minimum is in thousands
mask = df["salary"].str.contains("50,000", na=False)

df.loc[mask, "Min_Salary_LPA"] = 0.5

print("\nSalary After Cleaning:")
print(
    df[
        ["salary", "Min_Salary_LPA", "Max_Salary_LPA"]
    ].head(20)
)
# Clean Skills

def clean_skills(skill_text):

    if pd.isna(skill_text):
        return ""

    skills = skill_text.split(",")

    # Remove extra spaces
    skills = [skill.strip() for skill in skills]

    # Remove empty values
    skills = [skill for skill in skills if skill]

    # Remove duplicates
    skills = list(dict.fromkeys(skills))

    return ", ".join(skills)


df["Skills"] = df["Skills"].apply(clean_skills)


print("\nSkills After Cleaning:")
print(df["Skills"].head(10))

# Save final cleaned data
df.to_csv("cleaned_job_market_intelligence.csv", index=False)

print("\nFinal cleaned data saved successfully!")
print("Total Jobs:", len(df))