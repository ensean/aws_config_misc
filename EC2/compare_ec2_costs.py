#!/usr/bin/env python3
import boto3
import argparse
import json
from tabulate import tabulate
from datetime import datetime

def get_on_demand_price(pricing_client, instance_type, region):
    """
    Get the on-demand price for a specific EC2 instance type in a region
    """
    region_name_to_code = {
        'us-east-1': 'US East (N. Virginia)',
        'us-east-2': 'US East (Ohio)',
        'us-west-1': 'US West (N. California)',
        'us-west-2': 'US West (Oregon)',
        'af-south-1': 'Africa (Cape Town)',
        'ap-east-1': 'Asia Pacific (Hong Kong)',
        'ap-south-1': 'Asia Pacific (Mumbai)',
        'ap-northeast-3': 'Asia Pacific (Osaka)',
        'ap-northeast-2': 'Asia Pacific (Seoul)',
        'ap-southeast-1': 'Asia Pacific (Singapore)',
        'ap-southeast-2': 'Asia Pacific (Sydney)',
        'ap-northeast-1': 'Asia Pacific (Tokyo)',
        'ca-central-1': 'Canada (Central)',
        'eu-central-1': 'EU (Frankfurt)',
        'eu-west-1': 'EU (Ireland)',
        'eu-west-2': 'EU (London)',
        'eu-south-1': 'EU (Milan)',
        'eu-west-3': 'EU (Paris)',
        'eu-north-1': 'EU (Stockholm)',
        'me-south-1': 'Middle East (Bahrain)',
        'sa-east-1': 'South America (Sao Paulo)',
        'ap-southeast-5': 'Asia Pacific (Malaysia)'
    }
    
    region_description = region_name_to_code.get(region, region)
    
    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_description},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
            {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'Used'},
            {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
            {'Type': 'TERM_MATCH', 'Field': 'marketoption', 'Value': 'OnDemand'}
        ],
        MaxResults=100
    )
    
    if not response['PriceList']:
        return None
    
    price_data = json.loads(response['PriceList'][0])
    on_demand_data = price_data['terms']['OnDemand']
    on_demand_key = list(on_demand_data.keys())[0]
    price_dimensions = on_demand_data[on_demand_key]['priceDimensions']
    price_dimension_key = list(price_dimensions.keys())[0]
    
    return float(price_dimensions[price_dimension_key]['pricePerUnit']['USD'])

def format_price(price):
    """Format price with 4 decimal places"""
    if price is None:
        return "N/A"
    return f"${price:.5f}"

def main():
    parser = argparse.ArgumentParser(description='Compare EC2 instance costs across regions and instance types')
    parser.add_argument('--instance-types', '-i', required=True, help='Comma-separated list of EC2 instance types (e.g., t3.micro,m5.large)')
    parser.add_argument('--regions', '-r', required=True, help='Comma-separated list of AWS regions (e.g., us-east-1,eu-west-1)')
    
    args = parser.parse_args()
    
    # Parse regions and instance types
    regions = [region.strip() for region in args.regions.split(',')]
    instance_types = [instance_type.strip() for instance_type in args.instance_types.split(',')]
    
    # Initialize the pricing client (us-east-1 is the only endpoint for the pricing service)
    pricing_client = boto3.client('pricing', region_name='us-east-1')
    
    print(f"\nFetching on-demand pricing information for {len(instance_types)} instance types in {len(regions)} regions...\n")
    
    # Get pricing data for each region and instance type
    pricing_data = {}
    for region in regions:
        pricing_data[region] = {}
        for instance_type in instance_types:
            print(f"Fetching data for {instance_type} in {region}...")
            price = get_on_demand_price(pricing_client, instance_type, region)
            pricing_data[region][instance_type] = price
    
    # Prepare data for tabulation
    headers = ["Region"] + instance_types
    table_data = []
    
    for region in regions:
        row = [region]
        for instance_type in instance_types:
            price = pricing_data[region].get(instance_type)
            row.append(format_price(price))
        table_data.append(row)
    
    # Print the comparison table
    print("\n=== On-Demand Hourly Price Comparison (USD) ===\n")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    print(f"\nPricing information retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Note: Prices are in USD and do not include taxes or additional charges.")

if __name__ == "__main__":
    main()
