# SR_DE_coding_challenge

```

## CSV Files Structure

### hired_employees.csv
- `id` INTEGER - Id of the employee
- `name` STRING - Name and surname of the employee
- `datetime` STRING - Hire datetime in ISO format
- `department_id` INTEGER - Id of the department which the employee was hired for
- `job_id` INTEGER - Id of the job which the employee was hired for

Example:
```
4535,Marcelo Gonzalez,2021-07-27T16:02:08Z,1,2
4572,Lidia Mendez,2021-07-27T19:04:09Z,1,2
```

### departments.csv
- `id` INTEGER - Id of the department
- `department` STRING - Name of the department

Example:
```
1,Supply Chain
2,Maintenance
3,Staff
```

### jobs.csv
- `id` INTEGER - Id of the job
- `job` STRING - Name of the job

Example:
```
1,Recruiter
2,Manager
3,Analyst
```
