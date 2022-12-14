import boto3

def create_boto3_session():
    """
    If an access key and secret key are stored in .aws/credentials, boto3
    will automatically pick them up. Otherwise they must be passed into Session()
    """
    session = boto3.Session()
    return session.resource('s3')

def upload_to_s3(s3, obj: str, bucket: str, key: str) -> None:
    """Uploads JSON to specified S3 destination."""
    s3.put_object(Body=obj, Bucket=bucket, Key=key)