# Jenkins ETL Pipeline Project

A complete data engineering pipeline using Docker, Jenkins, Python, PostgreSQL, MySQL, and dbt.

## Project Overview

This project demonstrates a CI/CD automated ETL (Extract, Transform, Load) pipeline:

1. MySQL - Source database with sales data
2. Python ETL - Extracts, transforms, and loads data
3. PostgreSQL - Data warehouse
4. dbt - Data transformations and quality tests
5. Jenkins - Automates the entire pipeline

## Project Structure

```
jenkins_project/
├── docker-compose.yml      # Orchestrates all services
├── Jenkinsfile             # CI/CD pipeline definition
├── etl/
│   ├── Dockerfile          # Python container
│   ├── etl_script.py       # ETL logic
│   └── requirements.txt    # Python dependencies
├── jenkins/
│   └── Dockerfile          # Jenkins with Docker support
├── mysql/
│   └── init.sql            # Sample data
└── dbt_project/
    ├── dbt_project.yml     # dbt configuration
    ├── profiles.yml        # Database connection
    └── models/
        ├── staging/        # Staging models
        └── marts/          # Final models
```

## Prerequisites

- Docker Desktop installed
- Git (optional)

## Quick Start

### 1. Start the databases

```bash
docker-compose up -d mysql postgres
```

Wait 15 seconds for databases to be healthy.

### 2. Run ETL manually (optional)

```bash
docker-compose run --rm etl
```

### 3. Run dbt manually (optional)

```bash
docker-compose run --rm dbt run --profiles-dir /root/.dbt --project-dir /usr/app
```

### 4. Start Jenkins

```bash
docker-compose up -d jenkins
```

### 5. Access Jenkins

Open http://localhost:8080 in your browser.

### 6. Create Pipeline Job

1. Click "New Item"
2. Name: ETL_Pipeline
3. Select: Pipeline
4. Click OK
5. Scroll to Pipeline section
6. Paste the content of Jenkinsfile
7. Click Save
8. Click Build Now

## Services and Ports

| Service    | Port  | Description          |
|------------|-------|----------------------|
| MySQL      | 13306 | Source database      |
| PostgreSQL | 5433  | Data warehouse       |
| Jenkins    | 8080  | CI/CD interface      |

## Pipeline Stages

1. Check - Verify Docker is available
2. Start Databases - Ensure MySQL and PostgreSQL are running
3. Run ETL - Extract from MySQL, transform, load to PostgreSQL
4. Run dbt - Create staging and final tables
5. Validate - Verify data was loaded correctly

## Data Flow

```
MySQL (source)
    |
    v
Python ETL (extract + transform)
    |
    v
PostgreSQL raw_data table
    |
    v
dbt stg_sales (staging view)
    |
    v
dbt final_sales (final table with value_category)
```

## Database Credentials

MySQL:
- Host: mysql (or localhost:13306)
- User: etl_user
- Password: etl_password
- Database: source_db

PostgreSQL:
- Host: postgres (or localhost:5433)
- User: warehouse_user
- Password: warehouse_pass
- Database: warehouse_db

## Useful Commands

Stop all services:
```bash
docker-compose down
```

Stop and remove volumes (delete all data):
```bash
docker-compose down -v
```

View logs:
```bash
docker-compose logs mysql
docker-compose logs postgres
docker-compose logs jenkins
```

Rebuild a service:
```bash
docker-compose build etl
docker-compose build jenkins
```

Check running containers:
```bash
docker ps
```

Query PostgreSQL:
```bash
docker exec postgres_warehouse psql -U warehouse_user -d warehouse_db -c "SELECT * FROM final_sales;"
```

## Troubleshooting

### Port already in use

Change the port in docker-compose.yml:
```yaml
ports:
  - "13307:3306"  # Change 13306 to another port
```

### Container name conflict

Remove the old container:
```bash
docker rm mysql_source
docker rm postgres_warehouse
```

### dbt cannot find files

Make sure you run docker-compose from the project directory.

### Jenkins cannot access Docker

Ensure docker.sock is mounted in docker-compose.yml:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

## Learning Resources

- Docker: https://docs.docker.com/get-started/
- Jenkins Pipeline: https://www.jenkins.io/doc/book/pipeline/
- dbt: https://docs.getdbt.com/docs/introduction

## Author
### Houssam Ibnchakroune
Created as a learning project for CI/CD and data engineering.
