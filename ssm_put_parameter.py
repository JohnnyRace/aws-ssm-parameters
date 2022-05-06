# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import sys
import json
import boto3
import logging
from botocore.exceptions import ClientError


def put_parameter(parameter_name, parameter_value, parameter_type):
    """Creates new parameter in AWS SSM

    :param parameter_name: Name of the parameter to create in AWS SSM
    :param parameter_value: Value of the parameter to create in AWS SSM
    :param parameter_type: Type of the parameter to create in AWS SSM ('String'|'StringList'|'SecureString')
    :return: Return version of the parameter if successfully created else None
    """
    ssm_client = boto3.client('ssm')

    try:
        result = ssm_client.put_parameter(
            Name=parameter_name,
            Value=parameter_value,
            Type=parameter_type
        )
    except ClientError as e:
        logging.error(e)
        return None
    return result['Version']


def put_parameter_with_overwrite(parameter_name, parameter_value, parameter_type):
    """Creates new parameter in AWS SSM

    :param parameter_name: Name of the parameter to create in AWS SSM
    :param parameter_value: Value of the parameter to create in AWS SSM
    :param parameter_type: Type of the parameter to create in AWS SSM ('String'|'StringList'|'SecureString')
    :return: Return version of the parameter if successfully created else None
    """
    ssm_client = boto3.client('ssm')

    try:
        result = ssm_client.put_parameter(
            Name=parameter_name,
            Value=parameter_value,
            Type=parameter_type,
            Overwrite=True
        )
    except ClientError as e:
        logging.error(e)
        return None
    return result['Version']


def main():

    try:
        with open(sys.argv[1], 'r') as file:
            data = json.load(file)
    except IndexError:
        print("Provide a .json file with parameters")
        return 1
        
    for parameter in data:
        
    # Assign these values before running the program
    # If the specified specified parameter already exist in SSM, ParameterAlreadyExists error will be thrown
        parameter_name = parameter['name']
        parameter_value = parameter['value']
        parameter_type = parameter['type']  # ('String'|'StringList'|'SecureString')

        # Set up logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s: %(message)s')

        result = put_parameter_with_overwrite(parameter_name, parameter_value, parameter_type)
        logging.info(result)



if __name__ == '__main__':
    main()
