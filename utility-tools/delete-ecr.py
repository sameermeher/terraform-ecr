import boto3

# Create an ECR client
client = boto3.client('ecr')

# List all ECR repositories
response = client.describe_repositories()
repositories = response['repositories']

# Delete each ECR repository
for repository in repositories:
    repository_name = repository['repositoryName']
    print(f"Deleting repository: {repository_name}")
    client.delete_repository(repositoryName=repository_name, force=True)