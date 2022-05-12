import json
import sys
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

args = vars(parser.parse_args())

# Base checks
if args['replace'] and not args['to']:
    parser.error('Provide both --replace and --to arguments')
elif not args['replace'] and args['to']:
    parser.error('Provide both --replace and --to arguments')



def replace(parameter):
    return parameter['name'].replace(args['replace'], args['to'])


def put_parameter(ssm_client, parameter_name, parameter_value, parameter_type, overwrite):
    try:
        if not args['upload'] and not args['delete'] and not args['restore']:
            return print(f"{parameter_name} : {parameter_value}")
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
        delete_parameter(ssm, parameter['name'])

def upload(ssm, data):
    for parameter in data:
        if args['replace'] and args['to']:
            parameter['name'] = replace(parameter)
            put_parameter(ssm, parameter['name'], parameter['value'], parameter['type'], args['overwrite'])
        else:
            save(data)
            put_parameter(ssm, parameter['name'], parameter['value'], parameter['type'], args['overwrite'])
    return data
            


def save(data):
    with open('parameters.json', 'w') as file:
        file.write(str(json.dumps(data)))
    return "Saved in parameters.json"

def get_data():
    if not args['read']:
        data = json.load(sys.stdin)
    else:
        with open(args['read']) as file:
            data = json.load(file)
    return data


def main():
    session = boto3.Session(profile_name=args['profile'])
    ssm = session.client('ssm')

    if args['save']:
        data = get_data()
        return print(save(data))
    elif args['restore']:
        data = get_data()
        upload(ssm, data)
    elif args['replace']:
        data = get_data()
        new_data = upload(ssm, data)
        if args['delete']:
            clear(ssm, new_data)
    elif args['delete']:
        data = get_data()
        clear(ssm, data)

    

if __name__ == '__main__':
    main()
