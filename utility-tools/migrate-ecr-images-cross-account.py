import boto3
import pytz
from datetime import datetime

# Set the source and target AWS accounts and regions
src_account_id = '811651797278'
src_region = 'us-east-1'
dst_account_id = '811651797278'
dst_region = 'ap-south-1'

# Set the start date for filtering images
#start_date = datetime.datetime(2023, 1, 1)
specific_date = datetime(2023, 1, 1)
specific_date = pytz.UTC.localize(specific_date)

# Create an ECR client for the source account and region
src_client = boto3.client('ecr', region_name=src_region)

# Create an ECR client for the destination account and region
dst_client = boto3.client('ecr', region_name=dst_region)

# List all ECR repositories in the source account
response = src_client.describe_repositories(repositoryNames=['a203843/me-service'])
repositories = response['repositories']

# Iterate through each repository
for repository in repositories:
    repository_name = repository['repositoryName']
    print(f"Migrating images from repository: {repository_name}")

    # List the images in the repository
    response = src_client.describe_images(repositoryName=repository_name)
    images = response['imageDetails']
    filtered_images = [image for image in images if image['imagePushedAt'] >= specific_date]
    
    # Iterate through each image
    for image in filtered_images:
        #print(f"Migrating image: {image}")
        #image_pushed_at = image['imagePushedAt']
        #if image_pushed_at >= start_date:
        # Get the image manifest
        response = src_client.batch_get_image(repositoryName=repository_name, imageIds=[{'imageDigest': image['imageDigest']}])
        print(f"Response image: {response}")
        image_manifest = response['images'][0]['imageManifest']
        
        # Push the image to the destination repository
        dst_client.put_image(repositoryName=repository_name, imageManifest=image_manifest)

        # Delete the image from the source repository
        #src_client.batch_delete_image(repositoryName=repository_name, imageIds=[image])

print("Image migration complete.")