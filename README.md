# aws-ssm-parameters

## Usage
Just put JSON file with your parameters in the same folder with the script and run the script:
```python
python3 ssm_put_parameters.py
```
Also you can get all your names of variables using bash
```bash
aws ssm get-parameters-by-path --path "/sports68/qa/app/" | jq '.Parameters | [.[] | {name: .Name, value:.Value}]'
```
If you need to specify profile, use `--profile` parameter for `aws` command
