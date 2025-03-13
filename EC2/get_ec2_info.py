#!/usr/bin/env python3
"""
Script to retrieve EC2 instance information including:
- CPU count (vCPUs)
- Memory size
- EBS volume numbers and IDs

Requirements:
- AWS CLI configured with appropriate credentials
- boto3 library installed (pip install boto3)
- tabulate library installed (pip install tabulate)
"""

import boto3
import argparse
from tabulate import tabulate
import sys
import csv
import os

def get_instance_info(instance_id=None, region=None):
    """
    Retrieve information about EC2 instances.
    
    Args:
        instance_id (str, optional): Specific EC2 instance ID to query
        region (str, optional): AWS region to query
        
    Returns:
        list: List of dictionaries containing instance information
    """
    try:
        # Initialize boto3 EC2 client
        ec2_client = boto3.client('ec2', region_name=region) if region else boto3.client('ec2')
        ec2_resource = boto3.resource('ec2', region_name=region) if region else boto3.resource('ec2')
        
        # Get instances
        if instance_id:
            instances = ec2_resource.instances.filter(InstanceIds=[instance_id])
        else:
            instances = ec2_resource.instances.all()
        
        instance_info = []
        
        for instance in instances:
            # Skip terminated instances
            if instance.state['Name'] == 'terminated':
                continue
                
            # Get instance type details
            instance_type_info = ec2_client.describe_instance_types(
                InstanceTypes=[instance.instance_type]
            )['InstanceTypes'][0]
            
            # Get CPU and memory info
            vcpus = instance_type_info['VCpuInfo']['DefaultVCpus']
            memory_mib = instance_type_info['MemoryInfo']['SizeInMiB']
            memory_gib = round(memory_mib / 1024, 2)
            
            # Get EBS volumes
            volumes = list(instance.volumes.all())
            volume_count = len(volumes)
            total_volume_size = sum(v.size for v in volumes)
            volume_ids = [v.id for v in volumes]
            volume_ids_str = ', '.join(volume_ids) if volume_ids else 'None'
            
            # Get instance name from tags
            name_tag = next((tag['Value'] for tag in instance.tags or [] if tag['Key'] == 'Name'), 'N/A')
            
            instance_info.append({
                'Instance ID': instance.id,
                'Name': name_tag,
                'Instance Type': instance.instance_type,
                'State': instance.state['Name'],
                'vCPUs': vcpus,
                'Memory (GiB)': memory_gib,
                'EBS Volumes': volume_count,
                'Total EBS Size (GB)': total_volume_size,
                'Volume IDs': volume_ids_str
            })
            
        return instance_info
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def save_to_csv(instance_info, output_file):
    """
    Save instance information to a CSV file.
    
    Args:
        instance_info (list): List of dictionaries containing instance information
        output_file (str): Path to the output CSV file
    """
    try:
        if not instance_info:
            print("No data to save.")
            return False
            
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = instance_info[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for instance in instance_info:
                writer.writerow(instance)
                
        print(f"Data saved to {os.path.abspath(output_file)}")
        return True
        
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Get EC2 instance information')
    parser.add_argument('-i', '--instance-id', help='Specific EC2 instance ID to query')
    parser.add_argument('-r', '--region', help='AWS region to query')
    parser.add_argument('-o', '--output', help='Output CSV file path')
    args = parser.parse_args()
    
    try:
        # Get instance information
        instance_info = get_instance_info(args.instance_id, args.region)
        
        if not instance_info:
            print("No instances found or all instances are terminated.")
            return
        
        # Display information in a table
        headers = instance_info[0].keys()
        rows = [list(instance.values()) for instance in instance_info]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # Save to CSV if output file is specified
        if args.output:
            save_to_csv(instance_info, args.output)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
