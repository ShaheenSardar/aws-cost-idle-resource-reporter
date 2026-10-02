import boto3

from src.config import load_config


def get_aws_session():
    """Create a Boto3 session using config.yaml settings."""
    config = load_config()

    profile = config["aws"]["profile"]
    region = config["aws"]["region"]

    return boto3.Session(
        profile_name=profile,
        region_name=region,
    )


def get_ec2_client():
    """Return a Boto3 EC2 client."""
    session = get_aws_session()
    return session.client("ec2")


def get_cloudwatch_client():
    """Return a Boto3 CloudWatch client."""
    session = get_aws_session()
    return session.client("cloudwatch")