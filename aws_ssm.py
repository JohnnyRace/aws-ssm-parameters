import json
from os import remove, walk, getcwd
import os
import boto3
import logging
import argparse
from datetime import datetime

from botocore.exceptions import ClientError

# Parse arguments
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-P', '--profile', required=False)
parser.add_argument('-p', '--path', required=False)
parser.add_argument('-f', '--from', required=False)
parser.add_argument('-t', '--to', required=False)
parser.add_argument('-U', '--upload', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('-o', '--overwrite', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('-D', '--delete', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('-r', '--read', required=False)
parser.add_argument('-R', '--restore', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('-s', '--save', required=False)
parser.add_argument('-g', '--get', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('-c', '--clear', required=False,
                    action='store_const', default=False, const=True)                    

args = vars(parser.parse_args())

# Base checks
if args['from'] and not args['to']:
    parser.error('Provide both --replace and --to arguments')
elif not args['from'] and args['to']:
    parser.error('Provide both --replace and --to arguments')


def replace(parameter):
    return parameter['Name'].replace(args['from'], args['to'])

parameters_count = 0
upload_status = False
def put_parameter(ssm_client, parameter_name, parameter_value, parameter_type, overwrite):
    global parameters_count, upload_status

    try:
        if not args['upload'] and not args['delete'] and not args['restore']:
            return print(f"{parameter_name}")
        elif args['delete']:
            return
        else:
            result = ssm_client.put_parameter(
                Name=parameter_name,
                Value=parameter_value,
                Type=parameter_type,
                Overwrite=overwrite
            )
            upload_status = True
            parameters_count += 1
    except ClientError as e:
        logging.error(e)
        return None
    return result['Version']


def delete_parameter(ssm_client, parameter_name):
    try:
        ssm_client.delete_parameter(
            Name=parameter_name
        )
    except ClientError as e:
        logging.error(e)

def clear(ssm, data):
    print(save(data))
    if input(f"{data}\n\nDelete (Y/N): ") in ['y', 'YES', 'yes', 'Y']:
        for parameter in data:
            delete_parameter(ssm, parameter['Name'])
    else:
        return

def upload(ssm, data):
    for parameter in data:
        if args['from'] and args['to']:
            parameter['Name'] = replace(parameter)
            put_parameter(ssm, parameter['Name'], parameter['Value'], parameter['Type'], args['overwrite'])
        else:
            put_parameter(ssm, parameter['Name'], parameter['Value'], parameter['Type'], args['overwrite'])
    return data
            

def save(data):
    try:
        now = datetime.now()
        time_stamp = now.strftime("%H:%M:%S")
        if args['save']:
            name = args['save']
        else:
            name = f"parameters_dump_{time_stamp}"
        with open(f"{name}.json", 'w') as file:
            json.dump(data, file, indent=2, sort_keys=True, default=str)
        return f"\nSaved in {name}.json\n"
    except Exception as e:
        logging.error(e)
        return None


def get_data(ssm):
    try:
        if not args['read']:
            paginator = ssm.get_paginator('get_parameters_by_path')
            response_iterator = paginator.paginate(
                Path=args['path'],
                WithDecryption=True
            )
            data=[]
            for page in response_iterator:
                for entry in page['Parameters']:
                    data.append(entry)
        else:
            with open(args['read']) as file:
                data = json.load(file)
        return data
    except Exception as e:
        logging.error(e)
        return None


def main():
    try:
        session = boto3.Session(profile_name=args['profile'])
        ssm = session.client('ssm')
    except Exception as e:
        logging.error(e)
        return None

    if args['save']:
        data = get_data(ssm)
        return print(save(data))
    elif args['restore']:
        data = get_data(ssm)
        upload(ssm, data)
    elif args['from']:
        data = get_data(ssm)
        new_data = upload(ssm, data)
        if args['delete']:
            clear(ssm, new_data)
    elif args['delete']:
        data = get_data(ssm)
        clear(ssm, data)
    elif args['get']:
        data = get_data(ssm)
        return print(json.dumps(data, indent=2, sort_keys=True, default=str))
    elif args['read']:
        data = get_data(ssm)
        return print(json.dumps(data, indent=2, sort_keys=True, default=str))
    elif args['clear']:
        for filename in os.listdir():
            if 'parameters_dump_' in filename:
                print(f"Removed: {filename}")
                os.remove(os.path.abspath(filename))
        return None
    
        

if __name__ == '__main__':
    main()
    if upload_status:
        print(f"Uploaded {parameters_count} parameters")
