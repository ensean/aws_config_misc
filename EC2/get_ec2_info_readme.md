# EC2 Instance Information Script

This script retrieves and displays information about EC2 instances, including:
- CPU count (vCPUs)
- Memory size (GiB)
- EBS volume count, total size, and volume IDs
- Instance name, ID, type, and state

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Python 3.6+
3. Required Python packages:
   - boto3
   - tabulate

## Installation

Install the required packages:

```bash
pip install boto3 tabulate
```

## Usage

```bash
# Get information for all EC2 instances in the default region
python get_ec2_info.py

# Get information for a specific instance
python get_ec2_info.py --instance-id i-0123456789abcdef0

# Get information for instances in a specific region
python get_ec2_info.py --region us-west-2

# Save results to a CSV file
python get_ec2_info.py --output ec2_info.csv

# Combine options
python get_ec2_info.py --instance-id i-0123456789abcdef0 --region us-west-2 --output ec2_info.csv
```

## Output Example

```
+----------------------+----------------+---------------+--------+-------+---------------+-------------+--------------------+----------------------------------+
| Instance ID          | Name           | Instance Type | State  | vCPUs | Memory (GiB)  | EBS Volumes | Total EBS Size (GB) | Volume IDs                       |
+======================+================+===============+========+=======+===============+=============+====================+==================================+
| i-0123456789abcdef0  | web-server-01  | t3.medium     | running| 2     | 4.0           | 2           | 16                 | vol-1234abcd, vol-5678efgh       |
+----------------------+----------------+---------------+--------+-------+---------------+-------------+--------------------+----------------------------------+
| i-0123456789abcdef1  | db-server-01   | m5.large      | running| 2     | 8.0           | 3           | 100                | vol-abcd1234, vol-efgh5678, vol-ijkl9012 |
+----------------------+----------------+---------------+--------+-------+---------------+-------------+--------------------+----------------------------------+
```

## Notes

- The script skips terminated instances
- Memory is displayed in GiB (Gibibytes)
- EBS volume size is displayed in GB (Gigabytes)
- Instance names are retrieved from the "Name" tag (if available)
- CSV output includes all the same information as the table display
- If no output file is specified, results are only displayed in the terminal
