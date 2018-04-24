from aws_resource_finders import *

def lambda_handler(event, context):

  stop_ec2_instances_by_tag('Scheduled', 'True')
  stop_rds_instances_by_tag('Scheduled', 'True')