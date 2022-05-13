# aws-ssm-parameters

## Install
Just install [Python3](https://www.python.org/downloads/)

```bash
sudo apt install python3
```


## Usage

### Arguments

**R** - Required  
**O** - Optional  
**BR** - Both required

| Argument            | Description |
| :---                |    :----    |
| `-P`, `--profile`   | (R) Specify the AWS profile for script's session |
| `-p`, `--path`      | (R) SSM parameters path ex: `/my/first/param/ ` |
| `-g`, `--get`       | (O) Flag to get parameters without any actions with it |
| `-f`, `--from`      | (O/BR1) Specify a **part** of string to rename |
| `-t`, `--to`        | (O/BR1) Specify a new **part** of string |
| `-U`, `--upload`    | (O) Flag to upload new parameters |
| `-o`, `--overwrite` | (O) Flag to overwrite parameters |
| `-D`, `--delete`    | (O) Flag to delete the parameters |
| `-r`, `--read`      | (O) Flag to read the parameters from JSON file in current folder |
| `-R`, `--restore`   | (O/need -r before) Flag to restore the parameters from JSON file |
| `-s`, `--save`      | (O) Flag to save the parameters into JSON file |
| `-c`, `--clear`     | (O) Flag to delete all `parameters_dump_*.json` files in current directory |


Use both `--replace` and `--to` arguments!  

## Example

Replace `a` to `b` in all parameter names from `/` path in SSM
```bash
python3 aws_ssm.py --profile default --path /sokol/dev/ --replace a --to b --upload
```
Get all parameters by path
```bash
python3 aws_ssm.py --profile default --path / --get
```
Delete all replaced parameters
```bash
python3 aws_ssm.py --profile default --path /sokol/dev/ --replace dev --to qa --delete
```
