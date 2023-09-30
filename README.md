# AWS API Gateway Proxy Setup
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org)

 This repository contains a Python script that automates the setup of an API Gateway proxy in AWS using Boto3. The script creates the API Gateway, API key, usage plan, resources, methods, integrations, responses, and deployment. It also configures the AWS CLI for authentication.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- AWS CLI installed and configured with appropriate IAM credentials

## Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/H0llyW00dzZ/aws-api-gateway-proxy-setup.git
   ```

2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the AWS CLI profiles:

   ```bash
   python main.py ACCESS_KEY SECRET_KEY
   ```

   Replace `ACCESS_KEY` and `SECRET_KEY` with your AWS access key and secret key.

## Usage

To create the API Gateway proxy, run the following command:

```bash
python main.py ACCESS_KEY SECRET_KEY
```

Replace `ACCESS_KEY` and `SECRET_KEY` with your AWS access key and secret key.

The script will create the API Gateway proxy and print the URL of the deployed API Gateway.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute the code as per the terms of the license.
