#!/bin/bash

env=$1
file=""
fails=""

if [[ "${env}" == "dev" ]]; then
  file="docker-compose-dev.yml"
elif [[ "${env}" == "prod" ]]; then
  file="docker-compose-prod.yml"
else
  echo "USAGE: sh test.sh environment_name"
  echo "* environment_name: must either be 'dev', or 'prod'"
  exit 1
fi

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

/bin/sleep 5

docker-compose -f $file run orders flask cov
inspect $? orders
docker-compose -f $file run orders flake8
inspect $? orders-lint

docker-compose -f $file run products flask cov
inspect $? orders
docker-compose -f $file run products flake8
inspect $? orders-lint


if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi
