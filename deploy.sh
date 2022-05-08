#!/bin/bash

function validate {

    if [[ $1 ]]; then
        check_path="$1"
    else
        check_path="."
    fi

    echo "run validate on $check_path"

    echo "running black"
    black --diff --color --check -l 79 "$check_path"
    echo "running codespell"
    codespell --skip="./.git" "$check_path"
    echo "running flake8"
    flake8 "$check_path" --count --max-complexity=10 --max-line-length=79 \
        --show-source --statistics
    echo "running isort"
    isort --check-only --diff --profile black -l 79 "$check_path"
    printf "    \n> all validations passed\n"

}

function sync_test {
    
    host="tubearchivist.local"
    # make base folder
    ssh "$host" "mkdir -p docker"

    # copy project files to build image
    rsync -a --progress --delete-after \
        --exclude ".git" \
        --exclude ".gitignore" \
        --exclude "**/cache" \
        --exclude "**/__pycache__/" \
        . -e ssh "$host":tubearchivist-metrics

    ssh "$host" "docker buildx build -t bbilly1/tubearchivist-metrics:latest tubearchivist-metrics --load"

    ssh "$host" 'docker compose -f docker/docker-compose.yml up -d'

}

function sync_docker {

    # check things
    if [[ $(git branch --show-current) != 'master' ]]; then
        echo 'you are not on master, dummy!'
        return
    fi

    if [[ $(systemctl is-active docker) != 'active' ]]; then
        echo "starting docker"
        sudo systemctl start docker
    fi

    # checkout latest tag
    git fetch --tags github master
    VERSION=$(git tag | head -n 1)
    git checkout "$VERSION"

    echo "build and push tubearchivist-metrics:$VERSION ?"
    read -rn 1

    # start build
    sudo docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t bbilly1/tubearchivist-metrics \
        -t bbilly1/tubearchivist-metrics:"$VERSION" --push .

    git checkout master

}


if [[ $1 == "validate" ]]; then
    validate "$2"
elif [[ $1 == "test" ]]; then
    sync_test
elif [[ $1 == "docker" ]]; then
    sync_docker
else
    echo "valid options are: validate | test | docker"
fi

exit 0
