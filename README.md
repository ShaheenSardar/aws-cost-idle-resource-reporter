# AWS Cost & Idle Resource Reporter

A read-only AWS cost-optimization and idle-resource reporting tool built with Python and Boto3.

The application scans AWS resources for potential cost-optimization opportunities and generates JSON, CSV, and human-readable reports.

## Features

* EC2 resource scanning
* Detection of stopped EC2 instances
* EBS volume scanning
* Detection of unattached EBS volumes
* EBS snapshot scanning
* Detection of old snapshots
* CloudWatch CPU utilization analysis
* Configurable CPU utilization threshold
* Configurable snapshot age threshold
* Configurable CloudWatch lookback period
* AWS resource tag filtering
* JSON report generation
* CSV report generation
* Human-readable text report
* Application logging
* AWS/Boto3 error handling
* Unit testing with pytest
* AWS profile-based authentication
* Pagination for AWS API responses

## Architecture

```text
                    AWS Account
                         |
              +----------+----------+
              |                     |
          EC2 / EBS             CloudWatch
              |                     |
              +----------+----------+
                         |
                    Boto3 Clients
                         |
              +----------+----------+
              |          |          |
             EC2        EBS     Snapshots
              |          |          |
              +----------+----------+
                         |
                   Tag Filtering
                         |
                  Finding Detection
                         |
              +----------+----------+
              |          |          |
             JSON       CSV        TXT
              |          |          |
              +----------+----------+
                         |
                       Logs
```

## Project Structure

```text
aws-cost-idle-resource-reporter/
│
├── src/
│   ├── __init__.py
│   ├── aws_clients.py
│   ├── config.py
│   ├── ec2_scanner.py
│   ├── ebs_scanner.py
│   ├── snapshot_scanner.py
│   ├── cloudwatch_analyzer.py
│   ├── tag_filter.py
│   ├── json_reporter.py
│   ├── csv_reporter.py
│   ├── text_reporter.py
│   ├── logger.py
│   ├── error_handler.py
│   └── main.py
│
├── tests/
│   ├── test_tag_filter.py
│   ├── test_ec2_scanner.py
│   ├── test_ebs_scanner.py
│   ├── test_snapshot_scanner.py
│   ├── test_cloudwatch.py
│   └── test_reports.py
│
├── reports/
├── logs/
├── screenshots/
├── docs/
├── config.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

* Python 3.10+
* AWS account
* AWS CLI
* Boto3
* PyYAML
* pytest

## Installation

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## AWS Configuration

The application uses an AWS CLI profile instead of hardcoding credentials.

Example:

```bash
aws configure --profile aws-cost-reporter
```

Verify the profile:

```bash
aws sts get-caller-identity --profile aws-cost-reporter
```

The application should use a read-only IAM policy containing only the API permissions required for resource discovery and CloudWatch metrics.

**Never commit AWS access keys, secret keys, or session tokens to GitHub.**

## Application Configuration

Application settings are stored in `config.yaml`.

Example:

```yaml
aws:
  profile: aws-cost-reporter
  region: us-east-1

snapshot_age_days: 90

cloudwatch:
  lookback_days: 7
  cpu_threshold: 5.0
```

This allows thresholds and AWS settings to be changed without modifying the application code.

## Running the Application

Run the complete application:

```bash
python -m src.main
```

Run with an environment filter:

```bash
python -m src.main --environment dev
```

Filter by owner:

```bash
python -m src.main --owner Shaheen
```

Filter by project:

```bash
python -m src.main --project CloudLab
```

Multiple filters can be combined:

```bash
python -m src.main --environment dev --owner Shaheen --project CloudLab
```

## Generated Reports

The application generates:

```text
reports/
├── report.json
├── report.csv
└── summary.txt
```

### JSON

Contains summary counts for:

* Stopped EC2 instances
* Unattached EBS volumes
* Old snapshots
* Low-CPU instances

### CSV

Provides individual findings in a tabular format.

### Text

Provides a human-readable summary suitable for quick review.

## Logging

Application logs are stored in:

```text
logs/app.log
```

The logger records:

* Application startup
* Resource scanning
* Active filters
* Detected findings
* Report generation
* AWS/API errors
* Successful completion

## Testing

Run the complete test suite:

```bash
python -m pytest
```

The project includes unit tests for:

* Tag filtering
* EC2 detection
* EBS detection
* Snapshot detection
* CloudWatch CPU calculations
* Report generation

## Safety

This project is designed as a **read-only reporting tool**.

It does not automatically:

* Terminate EC2 instances
* Delete EBS volumes
* Delete snapshots
* Modify AWS infrastructure

Findings are reported for human review.

## AWS Cost Considerations

The application itself is designed to perform read-only discovery operations.

AWS resources created for testing may still incur charges. Test resources should be removed after testing is complete.

## Technologies

* Python
* Boto3
* AWS EC2
* AWS EBS
* AWS CloudWatch
* AWS IAM
* PyYAML
* pytest
* Git
* GitHub

## Testing Status

The project includes a complete automated test suite covering the main application components.

Example:

```text
13 passed
```

## Project Goal

The project demonstrates practical skills in:

* AWS resource discovery
* Cloud cost awareness
* IAM security
* Boto3 automation
* Python application structure
* Configuration management
* Logging
* Error handling
* Unit testing
* Report generation
* Git/GitHub project organization
