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

## Super abilities
* Easy to copy existing parameters for new environment
* Get parameters by path
* Script don't get parameters which are ManagedBy Terraform
* Save to file in `json` or `.env` format
* Read from `json` or `.env` file
* Rename part of parameters names
* Upload parameters from file or in action after renaming. Also you can overwrite existing parameters
* Delete parameters by path
* Assume role for session
* Specify a region for Parameter Store
* Script makes backups automaticaly when you delete or upload parameters

## Usage
**Main usage case:**
```bash
python3 ssm.py -P profile -r .env -a /project/env/app/ --region us-west-1 --id 1111111111111 --role ProductionRoleForExample -U -q
```
Replace `dev` to `qa` in all parameter names from `/sokol/dev/` path in SSM and upload new names. It will help you if if you need to copy parameters for new environment:
``` bash
python3 ssm.py --profile default --path /sokol/dev/ --from dev --to qa --upload
```
Short version:
```bash
python3 ssm.py -P default -p /sokol/dev/ -f dev -t qa -U
```
Do it in specified region:
```bash
python3 ssm.py -P default -p /sokol/dev/ -f dev -t qa -U --region us-west-2
```
Now do the same in prod account:
```bash
python3 ssm.py -P profile_name -p /project/dev/ -f dev -t qa --region us-west-1 --id 1111111111111 --role ProductionRoleForExample
```
it will create a backup file with parameters by origin path  
Get all parameters by path:
``` bash
python3 ssm.py --profile default --path /
```
![Output](./images/2022-05-18_15-48.png "Output")  
Save parameters to `.env` file:
```bash
python3 ssm.py -P default -p /sokol/dev/ -s .env
```
or
```bash
python3 ssm.py -P default -p /sokol/dev/ -s my_parameters.json
```
Delete parameters by path:
``` bash
python3 ssm.py -P default -p /sokol/dev/ -D
```
Delete parameters from file:
```bash
python3 ssm.py -P default -r .env -D
```
Upload parameters from file:
```bash
python3 ssm.py -P default -r .env -U
```


### How to assume role?

Read the documentation about [switching roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-cli.html) and about [organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tutorials_basic.html) in AWS.  
Also you can [read](https://aws.amazon.com/ru/premiumsupport/knowledge-center/lambda-function-assume-iam-role/) how it works for this script and what requirements it have.
Just use:
``` bash
python3 ssm.py -P johnrace -p /project/prod/ --id 1111111111111 --role ProductionRoleForExample
```
Now you 

### All arguments
**R** - Required  
**O** - Optional  
**BR**(number of group) - Both required

Use both `--replace` and `--to` arguments!

| Parameter           | Required | Description                                                                                              |
|---------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `-P`,`--profile`  | R        | Specify the AWS profile for script’s session                                                             |
| `-p`,`--path`      | R        | SSM parameters path ex: `/my/first/param/`                                                               |
| `--region`          | O        | Specify an AWS region                                                                                    |
| `--id`              | O/BR1    | Specify an account ID for assuming role                                                                  |
| `--role`            | O/BR1    | Specify a role name in children account                                                                  |
| `-r`,`--read`      | O        | Flag to read the parameters from `JSON` or `env` file in current folder. Use `filename.extension` format |
| `-s`,`--save`      | O        | Flag to save the parameters into `JSON` or `env` file                                                    |
| `-U`,`--upload`    | O        | Flag to upload new parameters. It will make a backup if you don’t use `-q` flag                          |
| `-D`,`--delete`    | O        | Flag to delete the parameters. Need input confirmation!                                                  |
| `-q`,`--quiet`     | O        | Flag to don't create backups                                                                             |
| `-c`,`--clear`     | O        | Flag to delete all `parameters_dump_*.json` files in current directory                                   |
| `-a`,`--add-path`  | O        | Add path to parameter. If you load from `.env` file this argument is required!                           |
| `-f`,`--from`      | O/BR2    | Specify a **part** of string to rename                                                                   |
| `-t`,`--to`        | O/BR2    | Specify a new **part** of string                                                                         |
| `-o`,`--overwrite` | O        | Flag to overwrite parameters                                                                             |
