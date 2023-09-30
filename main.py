##############################################################
# Author : H0llyW00dzZ                                       #
# Github : github.com/H0llyW00dzZ                            #
# License : MIT                                              #
# Tool : AWS API Gateway Proxy Setup.                        #
# Usage : python main.py <ACCESS_KEY> <SECRET_KEY>           #
##############################################################

import subprocess
import json
import boto3
import argparse

def create_api_gateway_proxy(api_name, stage_name):
    # Create a client for API Gateway
    apigateway_client = boto3.client('apigateway')

    # Create the REST API
    api_response = apigateway_client.create_rest_api(
        name=api_name,
        description='Proxy API created using Python script'
    )

    api_id = api_response['id']

    # Create an API key
    api_key_response = apigateway_client.create_api_key(
        name='MyAPIKey',
        description='API key for proxy authentication',
        enabled=True,
        stageKeys=[
            {
                'restApiId': api_id,
                'stageName': stage_name
            },
        ]
    )

    api_key = api_key_response['value']

    # Create the usage plan
    usage_plan_response = apigateway_client.create_usage_plan(
        name='MyUsagePlan',
        description='Usage plan for proxy API',
        apiStages=[
            {
                'apiId': api_id,
                'stage': stage_name
            },
        ],
        throttle={
            'rateLimit': 1000,
            'burstLimit': 2000
        },
        quota={
            'limit': 10000,
            'offset': 2,
            'period': 'MONTH'
        }
    )

    usage_plan_id = usage_plan_response['id']

    # Add the API key to the usage plan
    apigateway_client.create_api_key(
        apiKey=api_key,
        enabled=True,
        name='MyAPIKey',
        stageKeys=[
            {
                'restApiId': api_id,
                'stageName': stage_name
            },
        ],
        usagePlanIds=[
            usage_plan_id,
        ]
    )

    # Create the root resource
    root_resource_response = apigateway_client.get_resources(
        restApiId=api_id
    )

    root_resource_id = root_resource_response['items'][0]['id']

    # Create a resource for the proxy
    proxy_resource_response = apigateway_client.create_resource(
        restApiId=api_id,
        parentId=root_resource_id,
        pathPart='{proxy+}'
    )

    proxy_resource_id = proxy_resource_response['id']

    # Create a method for the proxy resource
    apigateway_client.put_method(
        restApiId=api_id,
        resourceId=proxy_resource_id,
        httpMethod='ANY',
        authorizationType='API_KEY'
    )

    # Create an integration for the method
    apigateway_client.put_integration(
        restApiId=api_id,
        resourceId=proxy_resource_id,
        httpMethod='ANY',
        integrationHttpMethod='ANY',
        type='HTTP_PROXY',
        uri='http://{proxy}',
        requestParameters={
            'integration.request.path.proxy': 'method.request.path.proxy'
        }
    )

    # Create a method response
    apigateway_client.put_method_response(
        restApiId=api_id,
        resourceId=proxy_resource_id,
        httpMethod='ANY',
        statusCode='200',
        responseModels={
            'application/json': 'Empty'
        }
    )

    # Create an integration response
    apigateway_client.put_integration_response(
        restApiId=api_id,
        resourceId=proxy_resource_id,
        httpMethod='ANY',
        statusCode='200',
        responseTemplates={
            'application/json': ''
        }
    )

    # Create a deployment for the API
    deployment_response = apigateway_client.create_deployment(
        restApiId=api_id,
        stageName=stage_name
    )

    # Get the URL of the deployed API
    api_url = 'https://{0}.execute-api.{1}.amazonaws.com/{2}'.format(
        api_id,
        boto3.session.Session().region_name,
        stage_name
    )

    return api_url, api_key

def configure_aws_cli(api_key):
    # Create the AWS CLI profile
    subprocess.run(['aws', 'configure', 'set', 'profile.default.aws_access_key_id', args.aws_access_key_id])
    subprocess.run(['aws', 'configure', 'set', 'profile.default.aws_secret_access_key', args.aws_secret_access_key])
    subprocess.run(['aws', 'configure', 'set', 'profile.default.aws_session_token', ''])
    subprocess.run(['aws', 'configure', 'set', 'profile.default.region', boto3.session.Session().region_name])

    # Create the AWS CLI named profile with API key authentication
    subprocess.run(['aws', 'configure', 'set', 'profile.api_key.aws_access_key_id', api_key])
    subprocess.run(['aws', 'configure', 'set', 'profile.api_key.aws_secret_access_key', ''])
    subprocess.run(['aws', 'configure', 'set', 'profile.api_key.aws_session_token', ''])
    subprocess.run(['aws', 'configure', 'set', 'profile.api_key.region', boto3.session.Session().region_name])
    subprocess.run(['aws', 'configure', 'set', 'profile.api_key.source_profile', 'default'])

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Create an API Gateway proxy')
parser.add_argument('aws_access_key_id', help='AWS Access Key ID')
parser.add_argument('aws_secret_access_key', help='AWS Secret Access Key')
args = parser.parse_args()

# Usage example
api_name = 'MyProxyAPI'
stage_name = 'dev'
api_url, api_key = create_api_gateway_proxy(api_name, stage_name)
print('API Gateway Proxy URL:', api_url)

configure_aws_cli(api_key)
