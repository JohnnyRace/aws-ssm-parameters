# aws-ssm-parameters

Simple python script for multiple parameter control in Amazon Parameter
Store Install Just install
[Python3](https://www.python.org/downloads/) and `boto3` module.

``` bash
sudo apt install -y python3 python3-pip python3-venv
```

Better practice is to use `venv`.

``` bash
python3 -m venv venv
```

``` bash
source venv/bin/activate
```

``` bash
pip3 install -r requirements.txt
```

To exit the venv just use `deactivate` command.

## Usage

### Arguments

**R** - Required  
**O** - Optional  
**BR**(number of group) - Both required

Use both `--replace` and `--to` arguments!

| Parameter           | Required | Description                                                                                              |
|---------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `-P`, `--profile`   | R        | Specify the AWS profile for script’s session                                                             |
| `-p`, `--path`      | R        | SSM parameters path ex: `/my/first/param/`                                                               |
| `--region`          | O        | Specify an AWS region                                                                                    |
| `--id`              | O/BR1    | Specify an account ID for assuming role                                                                  |
| `--role`            | O/BR1    | Specify a role name in children account                                                                  |
| `-r`, `--read`      | O        | Flag to read the parameters from `JSON` or `env` file in current folder. Use `filename.extension` format |
| `-s`, `--save`      | O        | Flag to save the parameters into `JSON` or `env` file                                                    |
| `-U`, `--upload`    | O        | Flag to upload new parameters. It will make a backup if you don’t use `-q` flag                          |
| `-D`, `--delete`    | O        | Flag to delete the parameters. Need input confirmation!                                                  |
| `-q`, `--quiet`     | O        | Flag to don't create backups                                                                             |
| `-c`, `--clear`     | O        | Flag to delete all `parameters_dump_*.json` files in current directory                                   |
| `-a`, `--add-path`  | O        | Add path to parameter. If you load from `.env` file this argument is required!                           |
| `-f`, `--from`      | O/BR2    | Specify a **part** of string to rename                                                                   |
| `-t`, `--to`        | O/BR2    | Specify a new **part** of string                                                                         |
| `-o`, `--overwrite` | O        | Flag to overwrite parameters                                                                             |

## Example

### Basic usage

Replace `a` to `b` in all parameter names from `/` path in SSM:
``` bash
python3 ssm.py --profile default --path /sokol/dev/ --from dev --to qa --upload
```
it will create a backup file with parameters by origin path  
Get all parameters by path:
``` bash
python3 ssm.py --profile default --path /
```
![Output](./images/2022-05-18_15-48.png "Output")  
You also can specify a region  
Delete parameters by path:
``` bash
python3 ssm.py -P default -p /sokol/dev/ -D
```
You will need to confirm this action

### How to assume role?

Read the documentation about [switching roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-cli.html) and about [organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tutorials_basic.html) in AWS.  
Also you can [read](https://aws.amazon.com/ru/premiumsupport/knowledge-center/lambda-function-assume-iam-role/) how it works for this script and what requirements it have.
Just use:
``` bash
python3 ssm.py -P johnrace -p /project/prod/ --id 1111111111111 --role ProductionRoleForExample
```