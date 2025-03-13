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
