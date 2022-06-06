import os
import json
import boto3
import logging
import argparse
from datetime import datetime
from dotenv import dotenv_values
from botocore.exceptions import ClientError

# Parse arguments
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-P', '--profile', required=False, default='default',
                    help="(R) Specify the AWS profile for script's session")
parser.add_argument('-p', '--path', required=False, default='/',
                    help="(R) SSM parameters path ex: `/my/first/param/`")
parser.add_argument('-a', '--add-path', required=False,
                    help="(R) add path to parameter")
parser.add_argument('-f', '--from', required=False,
                    help="(O/BR1) Specify a **part** of string to rename ")
parser.add_argument('-t', '--to', required=False,
                    help="(O/BR1) Specify a new **part** of string")
parser.add_argument('-U', '--upload', required=False,
                    action='store_const', default=False, const=True, help="(O) Flag to upload new parameters")
parser.add_argument('-o', '--overwrite', required=False,
                    action='store_const', default=False, const=True, help="(O) Flag to overwrite parameters")
parser.add_argument('-D', '--delete', required=False,
                    action='store_const', default=False, const=True, help="(O) Flag to delete the parameters")
parser.add_argument('-r', '--read', required=False,
                    help="(O) Flag to read the parameters from `JSON` or `env` file in current folder. Use `filename.extension` format")
parser.add_argument('-s', '--save', required=False,
                    help="(O) Flag to save the parameters into `JSON` or `env` file.  Use `filename.extension` format")
parser.add_argument('-q', '--quiet', required=False,
                    action='store_const', default=False, const=True, help="(O) Flag to don't create backups")
parser.add_argument('-c', '--clear', required=False,
                    action='store_const', default=False, const=True, help="(O) Flag to delete all `parameters_dump_*.json` files in current directory")
parser.add_argument('--id', required=False,
                    help="(O/BR2) Specify an account ID for assuming role")
parser.add_argument('--role', required=False,
                    help="(O/BR2) Specify a role name in children account")
parser.add_argument('--region', required=False,
                    help="(O) Specify an AWS region")
args = vars(parser.parse_args())

# Base checks
if args['from'] and not args['to']:
    parser.error('Provide both --rename and --to arguments')
elif not args['from'] and args['to']:
    parser.error('Provide both --rename and --to arguments')
if args['id'] and not args['role']:
    parser.error('Provide both --id and --to role')
elif not args['id'] and args['role']:
    parser.error('Provide both --id and --to role')


def rename(data):
    for parameter in data:
        parameter['Name'] = parameter['Name'].replace(args['from'], args['to'])
    return data


def upload_parameter(ssm, parameter_name, parameter_value, parameter_type, overwrite):
    try:
        if args['add_path']:
            parameter_name = args['add_path'] + parameter_name
        result = ssm.put_parameter(
            Name=parameter_name,
            Value=parameter_value,
            Type=parameter_type,
            Overwrite=overwrite
        )
    except ClientError as e:
        logging.error(e)
        return None
    return result['Version']


def delete_parameters(ssm, data):
    try:
        ssm.delete_parameters(
            Names=[parameter['Name'] for parameter in data]
        )
    except ClientError as e:
        logging.error(e)


def upload(ssm, data):
    if not args['quiet']:
        save(data)
    parameters_count = 0
    for parameter in data:
        upload_parameter(
            ssm, parameter['Name'], parameter['Value'], parameter['Type'], args['overwrite'])
        parameters_count += 1
    print(f"Uploaded {parameters_count} parameters")
    return True


def clear(ssm, data):
    if not args['quiet']:
        save(data)
    if input(f"{json.dumps(data, indent=2, sort_keys=True, default=str)}\n\nDelete (Y/N): ") in ['y', 'YES', 'yes', 'Y']:
        delete_parameters(ssm, data)
    else:
        return


def save(data):
    try:
        if args['save']:
            name = args['save']
        else:
            now = datetime.now()
            time_stamp = now.strftime("%H:%M:%S")
            name = f"parameters_dump_{time_stamp}.json"
        with open(f"{name}", 'w') as file:
            if '.json' in name:
                json.dump(data, file, indent=2,
                          sort_keys=True, default=str)
            else:
                for parameter in data:
                    file.write(
                        f"{parameter['Name']}={parameter['Value']}\n")
        print(f"Saved in '{name}' file")
        return True
    except Exception as e:
        logging.error(e)
        return None


def valid_tags(tags):
    for tag in tags:
        if 'ManagedBy' in tag.values() and 'Terraform' in tag.values():
            return False
    return True


def get_data(ssm):
    try:
        if not args['read']:
            paginator = ssm.get_paginator('get_parameters_by_path')
            response_iterator = paginator.paginate(
                Path=args['path'],
                WithDecryption=True
            )
            data = []
            for page in response_iterator:
                for parameter in page['Parameters']:
                    tags = ssm.list_tags_for_resource(
                        ResourceType='Parameter', ResourceId=parameter['Name'])
                    parameter['Tags'] = tags['TagList']
                    if valid_tags(parameter['Tags']):
                        data.append(parameter)
        else:
            name = args['read']
            with open(name) as file:
                if '.json' in name:
                    data = json.load(file)
                elif '.env' in name:
                    data = []
                    for parameter, value in dotenv_values(".env").items():
                        if not value:
                            value = 'NOT_DEFINED'
                        data.append(
                            {
                                'Name': parameter,
                                'Value': value,
                                'Type': 'String'
                            }
                        )
        return data
    except Exception as e:
        logging.error(e)
        return None


def main(ssm):
    data = get_data(ssm)

    if args['from'] and args['to']:
        new_data = rename(data)
        if args['save']:
            save(new_data)
        elif args['upload']:
            upload(ssm, new_data)
    elif args['save']:
        save(data)
    elif args['upload']:
        upload(ssm, data)
    elif args['delete']:
        clear(ssm, data)
    elif args['clear']:
        for filename in os.listdir():
            if 'parameters_dump_' in filename:
                print(f"Removed: {filename}")
                os.remove(os.path.abspath(filename))
        return None
    elif not data:
        return print('\nNo data. Check profile and path\n')
    else:
        return print(json.dumps(data, indent=2, sort_keys=True, default=str))


if __name__ == '__main__':
    try:
        session = boto3.Session(profile_name=args['profile'])
        if args['region']:
            region = args['region']
        else:
            region = session.region_name
        if args['id'] and args['role']:
            sts = boto3.client('sts')
            assumed_role_object = sts.assume_role(
                RoleArn=f"arn:aws:iam::{args['id']}:role/{args['role']}",
                RoleSessionName="Python-session"
            )
            credentials = assumed_role_object['Credentials']
            ssm = session.client(
                'ssm',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name=region
            )
        else:
            ssm = session.client('ssm', region_name=region)
        main(ssm)
    except Exception as e:
        logging.error(e)
