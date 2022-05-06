# aws-ssm-parameters

## Usage
Provide JSON file with parameters in correct format as argument and run:
```python
python3 ssm_put_parameters.py parameters.json
```
Also you can get all your names of variables using bash
```bash
aws ssm get-parameters-by-path --path "/your/parameters/path/" | jq '.Parameters | [.[] | {name: .Name, value:.Value, type:.Type}]'
```
If you need to specify profile, use `--profile` parameter for `aws` command

## Example
```bash
aws ssm get-parameters-by-path --path "/your/parameters/path/" | jq '.Parameters | [.[] | {name: .Name, value:.Value, type:.Type}]' > parameters.json
```
```bash
python3 ssm_delete_parameter.py parameters.json
```
