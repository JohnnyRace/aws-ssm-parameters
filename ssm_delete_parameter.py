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


def delete_parameter(parameter_name):
    """Delete parameter in AWS SSM

    :param parameter_name: Name of the parameter to delete from AWS SSM
    """
    ssm_client = boto3.client('ssm')

    try:
        ssm_client.delete_parameter(
            Name=parameter_name
        )
    except ClientError as e:
        logging.error(e)


def main():
    # Assign these values before running the program
    try:
        with open(sys.argv[1], 'r') as file:
            data = json.load(file)
    except IndexError:
        print("Provide a .json file with parameters")
        return 1

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # delete parameter from SSM

    # delete multiple parameters from SSM
    for parameter in data:
        delete_parameter(parameter['name'])


if __name__ == '__main__':
    main()
