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


import json
import boto3
import logging
from botocore.exceptions import ClientError


def get_parameters(parameter_names, with_decryption):
    """Get multiple parameter details in AWS SSM

    :param parameter_names: List of parameter names to fetch details from AWS SSM
    :param with_decryption: return decrypted value for secured string params, ignored for String and StringList
    :return: Return parameter details if exist else None
    """
    ssm_client = boto3.client('ssm')

    try:
        result = ssm_client.get_parameters(
            Names=parameter_names,
            WithDecryption=with_decryption
        )
    except ClientError as e:
        logging.error(e)
        return None
    return result


def main():

    with open('./parameters.json', 'r') as file:
        data = json.load(file)
    # for key, value in data.items():

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # get multiple parameter details
    with_decryption = False
    parameter_names = list(data.keys())
    result = get_parameters(parameter_names, with_decryption)

    # print parameter value, version for all the params
    if result:
        for parameter_details in result['Parameters']:
            logging.info("Name: " + parameter_details['Name'])
            logging.info("Value: " + parameter_details['Value'])
            logging.info("Version: " + str(parameter_details['Version']))


if __name__ == '__main__':
    main()
