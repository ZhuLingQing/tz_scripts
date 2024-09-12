#!/usr/bin/env bash
CURDIR=$(cd "$(dirname $0)";pwd)
# set -e
# set -x
set -o pipefail

pushd ${CURDIR}/../.. > /dev/null
GF_AURORA_PATH=$(pwd)
BU_CASE_PATH=${GF_AURORA_PATH}/build_aurora_bringup/samples/bringup/software
if [ -n "$VERSION" ]; then
    FW_VERSION=${VERSION}
else
    FW_VERSION=$(git rev-parse --short=8 HEAD)
fi
PACKAGE_NAME="bringup_cases_$FW_VERSION"

function warning() {
    local yellow="33m"
    echo -e "\033[${yellow}$* \033[0m" 2>&1
}

function error() {
    local red="31m"
    echo -e "\033[${red}$* \033[0m" 1>&2
    popd; exit 1
}

function info() {
    local blue="94m"
    echo -e "\033[${blue}$* \033[0m" 1>&2
}

function success() {
    local green="32m"
    echo -e "\033[${green}$* \033[0m" 2>&1
    popd > /dev/null; exit 0
}

info "#1. build bringup cases if not exist. Prepare environment."
PACKAGE_FILE="$PACKAGE_NAME.tar.gz"
rm bringup_cases_*.tar.gz -f
if [ ! -d ${BU_CASE_PATH} ]; then
    warning "${BU_CASE_PATH} not exist. make bu -j$(nproc) first"
    rc=$(make bu -j)
    if [ $rc -ne 0 ]; then
        error "Fail to build bringup cases $rc"
    fi
fi
IMAGE_TAR_DIR=${GF_AURORA_PATH}/build_aurora_bringup/$PACKAGE_NAME
if [ ! -d ${IMAGE_TAR_DIR} ]; then
    mkdir ${IMAGE_TAR_DIR}
else
    rm -rf ${IMAGE_TAR_DIR}/*
fi

info "#2. look for cases."
PE_NUM=0
MCP_NUM=0
CASE_NUM=0
while IFS= read -r line; do
    cp $line ${IMAGE_TAR_DIR}/ > /dev/null
    PE_NUM=$((PE_NUM+1))
    FILE_NAME=$(basename $line)
    echo -n "${FILE_NAME%"_sign.bin"}" >> ${IMAGE_TAR_DIR}/image_list.log 
    echo -e >> ${IMAGE_TAR_DIR}/image_list.log 
    CASE_NUM=$((CASE_NUM+1))
done < <(find ${BU_CASE_PATH} -name "*_sign.bin")

while IFS= read -r line; do
    cp $line ${IMAGE_TAR_DIR}/ > /dev/null
    MCP_NUM=$((MCP_NUM+1))
    FILE_NAME=$(basename $line)
    grep "${FILE_NAME%"_pack.bin"}" ${IMAGE_TAR_DIR}/image_list.log > /dev/null
    if [ $? -ne 0 ]; then
        echo -n "${FILE_NAME%"_pack.bin"}" >> ${IMAGE_TAR_DIR}/image_list.log 
        echo -e >> ${IMAGE_TAR_DIR}/image_list.log
        CASE_NUM=$((CASE_NUM+1))
    fi
done < <(find ${BU_CASE_PATH} -name "*_pack.bin")

echo "    There are $MCP_NUM MCP images and $PE_NUM PE images found. Total $CASE_NUM cases."

info "#3. packaging cases."
cp ${GF_AURORA_PATH}/utility/tests/run_bringup_test.sh ${IMAGE_TAR_DIR}
tar -czf $PACKAGE_FILE -C ${IMAGE_TAR_DIR}/.. ./$PACKAGE_NAME

info "#4. clean up the environment."
rm -rf ${IMAGE_TAR_DIR}

success "generate $PACKAGE_NAME.tar.gz into ${GF_AURORA_PATH}"
