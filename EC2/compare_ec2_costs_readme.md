# EC2 Instance Cost Comparison Tool

This script allows you to compare the on-demand hourly costs of multiple EC2 instance types across different AWS regions.

## Prerequisites

- Python 3.6+
- AWS CLI configured with appropriate permissions
- Required Python packages:
  - boto3
  - tabulate

## Installation

1. Install the required packages:

```bash
pip install boto3 tabulate
```

2. Ensure your AWS credentials are configured:

```bash
aws configure
```

## Usage

```bash
python compare_ec2_costs.py --instance-types <type1,type2,...> --regions <region1,region2,...>
```

### Parameters:

- `--instance-types`, `-i`: Comma-separated list of EC2 instance types (e.g., t3.micro,m5.large,c5.xlarge)
- `--regions`, `-r`: Comma-separated list of AWS regions (e.g., us-east-1,eu-west-1,ap-northeast-1)

## Example

```bash
python compare_ec2_costs.py --instance-types t3.micro,t3.small,t3.medium --regions us-east-1,eu-west-1,ap-southeast-1
```

## Output

The script outputs a table with:
- Regions as rows
- Instance types as columns
- On-demand hourly prices in USD as cell values
- "N/A" for any instance type/region combination where pricing information is not available

## Notes

- All prices are in USD and do not include taxes or additional charges.
- The script uses the AWS Pricing API, which requires appropriate IAM permissions.
- The pricing information is retrieved at the time of execution and may change over time.


| Region         | g4dn.12xlarge   | g5.12xlarge   | g6.12xlarge   | g6e.12xlarge   | p4d.24xlarge   | p5.48xlarge   | p5en.48xlarge   |
|----------------|-----------------|---------------|---------------|----------------|----------------|---------------|-----------------|
| us-east-1      | $3.91200        | $5.67200      | $4.60160      | $10.49264      | $32.77260      | $98.32000     | N/A             |
| us-west-2      | $3.91200        | $5.67200      | $4.60160      | $10.49264      | $32.77260      | $98.32000     | $84.80000       |
| us-east-2      | $3.91200        | $5.67200      | $4.60160      | $10.49264      | $32.77260      | $98.32000     | $84.80000       |
| eu-central-1   | $4.89000        | $7.09282      | $5.75429      | $13.12002      | $40.94475      | N/A           | N/A             |
| ap-east-1      | $6.02400        | N/A           | N/A           | N/A            | N/A            | N/A           | N/A             |
| ap-northeast-1 | $5.28100        | $8.22609      | $6.67369      | $15.21742      | $44.92215      | $123.19496    | $106.00000      |
| ap-southeast-1 | $5.47400        | N/A           | N/A           | N/A            | $39.32710      | N/A           | N/A             |
| ap-southeast-5 | N/A             | N/A           | $5.79660      | N/A            | N/A            | N/A           | N/A             |

Pricing information retrieved on: 2025-03-14 00:30:51