import boto3

def get_tag_value(tags, key):
    """Get a specific Tag value from a list of Tags"""
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']
    else:
        raise KeyError

def stop_ec2_instances_by_tag(tag_key, tag_value):
   """Stop all EC2 Instances by tag key and value"""
   ec2_instances = get_ec2_instances_by_tag(tag_key, tag_value)
   print('Found EC2 Instances: ' + str(ec2_instances))
   ec2 = boto3.client('ec2')
   if ec2_instances:
      ec2.stop_instances(InstanceIds=ec2_instances)

def start_ec2_instances_by_tag(tag_key, tag_value):
   """Start all EC2 Instances by tag key and value"""
   ec2_instances = get_ec2_instances_by_tag(tag_key, tag_value)
   print('Found EC2 Instances: ' + str(ec2_instances))
   ec2 = boto3.client('ec2')
   if ec2_instances:
      ec2.start_instances(InstanceIds=ec2_instances)

def start_rds_instances_by_tag(tag_key, tag_value):
   """Start all RDS Instances by tag key and value"""
   rds_instances = get_rds_instances_by_tag(tag_key, tag_value)
   print('Found RDS Instances: ' + str(rds_instances))
   rds = boto3.client('rds')
   for instance in rds_instances:
      rds.start_db_instance(DBInstanceIdentifier=instance)

def stop_rds_instances_by_tag(tag_key, tag_value):
   """Stop all RDS Instances by tag key and value"""
   rds_instances = get_rds_instances_by_tag(tag_key, tag_value)
   print('Found RDS Instances: ' + str(rds_instances))
   rds = boto3.client('rds')
   for instance in rds_instances:
      rds.stop_db_instance(DBInstanceIdentifier=instance)
   
def get_ec2_instances_by_tag(tag_key, tag_value):
    """Return a list of EC2 instances with the matching tags and values"""
    ec2 = boto3.client('ec2')
    instances = []
    for reservation in ec2.describe_instances()['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            try:
                tags = instance['Tags']
                value = get_tag_value(tags, tag_key)
                if value == tag_value:
                    instances.append(instance_id)
            except KeyError:
                pass
    return instances

def get_rds_instances_by_tag(tag_key, tag_value):
    """Return a list of RDS instances with the matching tags and values"""
    rds = boto3.client('rds')
    instances = []
    for instance in rds.describe_db_instances()['DBInstances']:
        instance_id = instance['DBInstanceIdentifier']
        arn = instance['DBInstanceArn']
        try:
            tags = rds.list_tags_for_resource(ResourceName=arn)
            value = get_tag_value(tags['TagList'], 'Scheduled')
            if value == 'True':
                instances.append(instance_id)
        except KeyError:
            pass
    return instances