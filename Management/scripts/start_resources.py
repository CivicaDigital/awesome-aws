from aws_resource_finders import *

def lambda_handler(event, context):

    # Start all EC2 instances with the tag Scheduled with the value True
    start_ec2_instances_by_tag('Scheduled', 'True')
    
    # Start all RDS instances with the tag Scheduled with the value True
    start_rds_instances_by_tag('Scheduled', 'True')