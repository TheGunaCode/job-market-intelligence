USE job_market;

-- 1. Total Jobs
SELECT COUNT(*) AS total_jobs
FROM jobs;

-- 2. Company-wise Jobs
SELECT company_name, COUNT(*) AS total_jobs
FROM jobs
GROUP BY company_name
ORDER BY total_jobs DESC;

-- 3. Average Salary
SELECT AVG(max_salary_lpa) AS avg_max_salary
FROM jobs;

-- 4. Jobs by Location
SELECT location, COUNT(*) AS total_jobs
FROM jobs
GROUP BY location
ORDER BY total_jobs DESC;

-- 5. Jobs requiring Python
SELECT company_name, experience, skills, job_url
FROM jobs
WHERE skills LIKE '%Python%';