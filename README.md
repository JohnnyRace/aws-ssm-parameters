# aws-ssm-parameters

## Install
Install [jq](https://stedolan.github.io/jq/) and [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) using the documentation or for Linux (x86) just paste commands below into your terminal
```bash
sudo apt install jq
```
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```
```bash
unzip awscliv2.zip

```
```bash
sudo ./aws/install
```
```bash
git clone https://github.com/JohnnyRace/aws-ssm-parameters.git
```
```bash
cd aws-ssm-parameters
```
```bash
sudo chmod +x aws_ssm.sh
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
./aws_ssm.sh --profile default --path / --replace a --to b --upload --overwrite 
```
Get all parameters by path
```bash
./aws_ssm.sh --profile default --path / --get
```
***(Not finalized)*** Delete all replaced parameters
```bash
./aws_ssm.sh --profile default --path / --replace a --to b --delete
```