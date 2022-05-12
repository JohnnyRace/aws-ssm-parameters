import json
import subprocess
import boto3
import logging
import argparse

from botocore.exceptions import ClientError

# Enable loging
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(levelname)s: %(asctime)s: %(message)s')

# Parse arguments
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('--profile', required=False)
parser.add_argument('--path', required=False)
parser.add_argument('--replace', required=False)
parser.add_argument('--to', required=False)
parser.add_argument('--upload', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('--overwrite', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('--delete', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('--read', required=False)
parser.add_argument('--restore', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('--save', required=False,
                    action='store_const', default=False, const=True)
parser.add_argument('--get', required=False,
                    action='store_const', default=False, const=True)                    

args = vars(parser.parse_args())

# Base checks
if args['replace'] and not args['to']:
    parser.error('Provide both --replace and --to arguments')
elif not args['replace'] and args['to']:
    parser.error('Provide both --replace and --to arguments')



def replace(parameter):
    return parameter['Name'].replace(args['replace'], args['to'])


def put_parameter(ssm_client, parameter_name, parameter_value, parameter_type, overwrite):
    try:
        if not args['upload'] and not args['delete'] and not args['restore']:
            return print(f"{parameter_name} : {parameter_value}")
        elif args['delete']:
            return
        else:
            result = ssm_client.put_parameter(
                Name=parameter_name,
                Value=parameter_value,
                Type=parameter_type,
                Overwrite=overwrite
            )
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
    save(data)
    for parameter in data:
        delete_parameter(ssm, parameter['Name'])

def upload(ssm, data):
    for parameter in data:
        if args['replace'] and args['to']:
            parameter['Name'] = replace(parameter)
            put_parameter(ssm, parameter['Name'], parameter['Value'], parameter['Type'], args['overwrite'])
        else:
            save(data)
            put_parameter(ssm, parameter['Name'], parameter['Value'], parameter['Type'], args['overwrite'])
    return data
            


def save(data):
    with open('parameters.json', 'w') as file:
        file.write(str(json.dumps(data)))
    return "Saved in parameters.json"

def get_data(ssm):
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


def main():
    session = boto3.Session(profile_name=args['profile'])
    ssm = session.client('ssm')

    if args['save']:
        data = get_data(ssm)
        return print(save(data))
    elif args['restore']:
        data = get_data(ssm)
        upload(ssm, data)
    elif args['replace']:
        data = get_data(ssm)
        new_data = upload(ssm, data)
        if args['delete']:
            clear(ssm, new_data)
    elif args['delete']:
        data = get_data(ssm)
        clear(ssm, data)
    elif args['get']:
        data = get_data(ssm)
        return print(json.dumps(data))

    

if __name__ == '__main__':
    main()
