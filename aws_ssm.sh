#!/usr/bin/bash

GET=0
PLAN=0

while [ -n "$1" ]; do
    case "$1" in
    -h | --help)
        echo $(pyhton3 aws_parameters.py -h)
        ;;
    --profile)
        PROFILE=$2
        PROFILE_SH="--profile $PROFILE"
        shift
        ;;
    --path)
        PARAMETER_PATH=$2
        SSM_PATH="--path $PARAMETER_PATH"
        shift
        ;;
    --replace)
        REPLACE_FROM=$2
        REPLACE="--replace $REPLACE_FROM"
        shift
        ;;
    --to)
        REPLACE_TO=$2
        TO="--to $REPLACE_TO"
        shift
        ;;
    --read)
        READ_FILE=$2
        READ="--read $READ_FILE"
        shift
        ;;
    --upload)
        UPLOAD="--upload"
        ;;
    --overwrite)
        OVERWRITE="--overwrite"
        ;;
    --delete)
        DELETE="--delete"
        ;;
    --restore)
        RESTORE="--restore"
        ;;
    --save)
        SAVE="--save"
        ;;
    --get)
        let GET=1
        ;;
    *)
        echo "Unexpected option: $1"
        help
        ;;
    esac
    shift
done

main () {

    DATA=$(aws ssm get-parameters-by-path $PROFILE_SH $SSM_PATH | jq '.Parameters | [.[] | {name: .Name, value:.Value, type:.Type}]')
    if [ $GET -eq 1 ]; then
        echo $DATA | jq
    fi
    echo $DATA | python3 aws_parameters.py $PROFILE_SH $REPLACE $TO $UPLOAD $OVERWRITE $DELETE $RESTORE $READ $SAVE

}

main
