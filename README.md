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

| Argument      | Description |
| :---          |    :----   |
| `--profile`   | (R) Specify the AWS profile for script's session |
| `--path`      | (R) SSM parameters path ex: `/my/first/param/ ` |
| `--get`       | (O) Flag to get parameters without any actions with it |
| `--replace`   | (O/BR1) Specify a **part** of string to replace |
| `--to`        | (O/BR1) Specify a new **part** of string |
| `--upload`    | (O) Flag to upload new parameters |
| `--overwrite` | (O) Flag to overwrite parameters |
| `--delete`    | (O) Flag to delete the parameters |
| `--read`      | (O/BR2) Flag to read the parameters from JSON file in current folder |
| `--restore`   | (O/BR2) Flag to restore the parameters from JSON file |

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
