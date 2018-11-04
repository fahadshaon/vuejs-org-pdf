#!/usr/bin/env bash

PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONF_PATH="${PROJECT_PATH}/.env"

test ${CONF_PATH} && source ${CONF_PATH}

if [[ -z ${VENV} ]]; then
    VENV=${PROJECT_PATH}/venv
fi

python="${VENV}/bin/python"
run_script="${PROJECT_PATH}/run.py"


function usage {
    if [[ ! -f ${python} ]]; then
        echo "Usage: ${0} init to get started"
        exit
    fi

    ${python} ${run_script} -h
}


function cmd_help {
    usage
}


function clone_vuejs_org {

    base=${PROJECT_PATH}/build
    echo "Cloning vuejs.org repository into ${base}"

    mkdir -p ${base}
    pushd ${base} > /dev/null

    git clone https://github.com/vuejs/vuejs.org.git

    # Setting the variable for current bash
    VUEJS_ORG_PATH=${PROJECT_PATH}/build/vuejs.org

    # Saving in .env file for later usage
    echo 'VUEJS_ORG_PATH=${PROJECT_PATH}/build/vuejs.org' >> "${PROJECT_PATH}/.env"

    popd > /dev/null
}

function install_python_dependencies {

    echo "Creating python virtual environment"

    pushd ${PROJECT_PATH} > /dev/null
    virtualenv venv

    echo "Installing python dependencies"
    ${VENV}/bin/pip install -r requirements.txt

    popd > /dev/null
}

function build_vuejs_org {

    echo "Installing dependencies and building vuejs.org project"

    pushd ${VUEJS_ORG_PATH} > /dev/null

    npm install && npm run-script build

    popd > /dev/null
}

function copy_css_js_images {

    echo "Copying css, js, and images"

    mkdir -p ${PROJECT_PATH}/build/dist
    pushd ${PROJECT_PATH}/build/dist > /dev/null

    rsync -aP ${VUEJS_ORG_PATH}/public/js .
    rsync -aP ${VUEJS_ORG_PATH}/public/css .
    rsync -aP ${VUEJS_ORG_PATH}/public/images .

    popd > /dev/null
}

function cmd_init {

    echo "Initializing"

    if [[ -z ${VUEJS_ORG_PATH} || ! -d ${VUEJS_ORG_PATH} ]]; then
        clone_vuejs_org
    fi

    if [[ ! -d ${VUEJS_ORG_PATH}/public ]] ; then
        build_vuejs_org
    fi

    if [[ ! -d ${PROJECT_PATH}/build/dist ]]; then
        copy_css_js_images
    fi

    if [[ ! -d ${VENV} ]]; then
        install_python_dependencies
    fi
}

function cmd_install_wkhtmltopdf {
    if [[ $(lsb_release -is) != 'Ubuntu' ]]; then
        echo "Only ubuntu supported"
        exit 1
    fi

    release=$(lsb_release -cs)
    arch=$(dpkg --print-architecture)

    mkdir -p ${PROJECT_PATH}/build/wkhtml
    pushd ${PROJECT_PATH}/build/wkhtml > /dev/null

    url="https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.${release}_${arch}.deb"
    wget ${url}

    filename=$(basename ${url})
    sudo dpkg -i ${filename}
    sudo apt --fix-broken install

    popd > /dev/null
}


if [[ $1 == '-h' || $1 == '--help' || -z "$@" ]]; then
    usage
    exit 0
fi

if [[ $2 == '-h' || $2 == '--help' ]]; then
    "${python}" "${run_script}" "$@"
    exit 0
fi

command="cmd_${1}"

if [[ `type -t "${command}"` ==  "function" ]]; then
    ${command} "${@:2}"
    exit $?
fi

"${python}" "${run_script}" "$@"
