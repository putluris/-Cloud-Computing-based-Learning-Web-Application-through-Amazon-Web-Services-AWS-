import boto3

# Initialize a session using Amazon Route53
route53_client = boto3.client('route53')

# Create a hosted zone in Route53
def create_hosted_zone(domain_name):
    response = route53_client.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(hash(domain_name)),
        HostedZoneConfig={
            'Comment': 'Hosted zone for e-learning portal',
            'PrivateZone': False
        }
    )
    return response

# Initialize a session using Amazon RDS
rds_client = boto3.client('rds')

# Create an RDS MySQL instance
def create_rds_instance(db_identifier, db_name, master_username, master_password):
    response = rds_client.create_db_instance(
        DBInstanceIdentifier=db_identifier,
        AllocatedStorage=20,
        DBName=db_name,
        Engine='mysql',
        MasterUsername=master_username,
        MasterUserPassword=master_password,
        DBInstanceClass='db.t2.micro',
        PubliclyAccessible=True
    )
    return response

# Initialize a session using Amazon SNS
sns_client = boto3.client('sns')

# Create an SNS topic for push notifications
def create_sns_topic(topic_name):
    response = sns_client.create_topic(Name=topic_name)
    return response

# Initialize a session using Amazon S3
s3_client = boto3.client('s3')

# Create an S3 bucket for static content
def create_s3_bucket(bucket_name):
    response = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': boto3.session.Session().region_name
        }
    )
    return response

# Initialize a session using IAM
iam_client = boto3.client('iam')

# Create an IAM role
def create_iam_role(role_name):
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
        Description='Role to allow EC2 instances to access AWS services'
    )
    return response

if __name__ == "__main__":
    # Example usage of the above functions
    
    # Create Route53 hosted zone
    domain_name = "elearning.example.com"
    hosted_zone_response = create_hosted_zone(domain_name)
    print(f"Hosted Zone created: {hosted_zone_response['HostedZone']['Id']}")

    # Create RDS instance
    rds_response = create_rds_instance(
        db_identifier="elearning-db",
        db_name="elearning",
        master_username="admin",
        master_password="password"
    )
    print(f"RDS Instance creating: {rds_response['DBInstance']['DBInstanceIdentifier']}")

    # Create SNS topic
    sns_topic_response = create_sns_topic("ElearningNotifications")
    print(f"SNS Topic created: {sns_topic_response['TopicArn']}")

    # Create S3 bucket
    s3_bucket_name = "elearning-static-content"
    s3_bucket_response = create_s3_bucket(s3_bucket_name)
    print(f"S3 Bucket created: {s3_bucket_response['Location']}")

    # Create IAM role
    iam_role_response = create_iam_role("ElearningEC2Role")
    print(f"IAM Role created: {iam_role_response['Role']['RoleName']}")
