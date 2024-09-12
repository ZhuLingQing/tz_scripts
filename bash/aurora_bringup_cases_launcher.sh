#!/bin/bash
CURDIR=$(cd "$(dirname $0)";pwd)
#set -e
#set -x
set -o pipefail

EIC_TEST="aurora_eic_test"
MSG_DISPLAY=""

trap 'echo "\033[33mUser canceled \033[0m"; exit 2' INT

function warning() {
    local yellow="33m"
    echo -e "\033[${yellow}$* \033[0m" 2>&1
}

function error() {
    local red="31m"
    echo -e "\033[${red}$* \033[0m" 1>&2
}

function info() {
    local blue="94m"
    echo -e "\033[${blue}$* \033[0m" 1>&2
}

function success() {
    local green="32m"
    echo -e "\033[${green}$* \033[0m" 2>&1
}

function isdigit() {
  local re='^[0-9]+$'
  [[ $1 =~ $re ]] && return 0 || return 1
}

function help_menu() {
    echo "Usage: "
    echo "        ./run_bringup_test.sh [PATH_OF_AURORA_EIC_TEST]"
    echo "            Traverse all cases with PE_MASK=15."
    echo "    or"
    echo "        ./run_bringup_test.sh [PATH_OF_AURORA_EIC_TEST] [PE_MASK]"
    echo "            Traverse all cases with specified PE_MASK."
    echo "    or"
    echo "        ./run_bringup_test.sh [PATH_OF_AURORA_EIC_TEST] [NAME_OF_TEST_CASE]"
    echo "            Execute the specified test case and traverse the PE_MASK from 1 to 15."
    echo "    or"
    echo "        ./run_bringup_test.sh [PATH_OF_AURORA_EIC_TEST] [NAME_OF_TEST_CASE] [PE_MASK]"
    echo "            Execute the specified NAME_OF_TEST_CASE with specified PE_MASK."

    exit 1
}

# $1=image name.
function find_mcp() {
    fname=`find ${BU_CASE_PATH} -name "$1_pack.bin"`
    farray=(${fname// / })
    fnum=${#farray[@]}
    #echo find: $fnum
    if [ $((fnum)) -ne 1 ]; then
        echo "$1_pack.bin not found"
        return 1
    fi
    echo $fname
    return 0
}

# $1=image name.
function find_pe() {
    fname=`find ${BU_CASE_PATH} -name "$1_sign.bin"`
    farray=(${fname// / })
    fnum=${#farray[@]}
    #echo find: $fnum
    if [ $((fnum)) -ne 1 ]; then
        echo "$1_sign.bin not found"
        return 1
    fi
    echo $fname
    return 0
}

RESULT_MSG=()

function print_case_results() {
    local CASE_NUM=${#RESULT_MSG[@]}
    info "executed ${CASE_NUM} cases"
    for index in "${!RESULT_MSG[@]}"; do
        echo -e "($((index+1))/$CASE_NUM): ${RESULT_MSG[$index]}"
    done
}

# $1=image name.
# $2=pe mask.
function exeucte_case() {
    CASE_NAME=$1
    PE_MASK=$2
    PE_HOST_LIST=("bu_pdma_host")
    MCP_HOST_LIST=("bu_hif_connectivity" "bu_udma_global_pmem" "bu_udma_global_ilm" "bu_udma_local_pmem" "bu_udma_stress" "bu_udma_wbst")
    MCP_BIN="${CURDIR}/${CASE_NAME}_pack.bin"
    if [ ! -f $MCP_BIN ]; then
        error "$MCP_BIN: No such file"
        exit 1
    fi 
    PE_BIN="${CURDIR}/${CASE_NAME}_sign.bin"
    if [ ! -f $PE_BIN ]; then
        error "$PE_BIN: No such file"
        exit 1
    fi 
    # ./nbr.sh -c
    if echo "${PE_HOST_LIST[@]}" | grep -qw "$1"; then
        # pdma host need driver compare, one pe once.
        PE_ARRAY=(1 2 4 8)
        for MASK_ARRAY in "${PE_ARRAY[@]}"; do
            if [ 0 -ne $((i&PE_MASK)) ]; then
                eval "$AURORA_EIC_TEST --gtest_filter=WorkLoadTest.DmaTest --pe_fw_path=$PE_BIN --pe_mask=$MASK_ARRAY --fw_param=0 $MSG_DISPLAY"
            fi
        done
    elif echo "${MCP_HOST_LIST[@]}" | grep -qw "$1"; then
        if [[ $CASE_NAME == *wbst* ]]; then
            # udma wbst need driver compare.
            eval "$AURORA_EIC_TEST --gtest_filter=WorkLoadTest.DmaTest --mcp_fw_path=$MCP_BIN --mcp_mask=1 --pe_mask=0 --fw_param=$PE_MASK $MSG_DISPLAY"
        elif [[ $CASE_NAME == *global* ]]; then
            # udma global need driver compare, one pe once.
            PE_ARRAY=(1 2 4 8)
            for i in "${PE_ARRAY[@]}"; do
                if [ 0 -ne $((i&PE_MASK)) ]; then
                    eval "$AURORA_EIC_TEST --gtest_filter=WorkLoadTest.DmaTest --mcp_fw_path=$MCP_BIN --mcp_mask=1 --pe_mask=0 --fw_param=$i $MSG_DISPLAY"
                fi
            done
        else
            # udma local and stress need driver compare.
            eval "$AURORA_EIC_TEST --gtest_filter=WorkLoadTest.DmaTest --mcp_fw_path=$MCP_BIN --mcp_mask=1 --pe_mask=0 --fw_param=0 $MSG_DISPLAY"
        fi
    else
        # most cases no driver participation
        eval "$AURORA_EIC_TEST --gtest_filter=WorkLoadTest.LoadProgram --mcp_fw_path=$MCP_BIN --pe_fw_path=$PE_BIN --pe_mask=$PE_MASK --mcp_mask=1 $MSG_DISPLAY"
    fi
    rc=$?

    if (( rc != 0 )); then
        RESULT_MSG+=(" \033[33m$CASE_NAME\033[0m pe_mask=$PE_MASK \033[31m[FAIL]\033[0m")
        echo -e "\033[31m[[FAIL]] \033[33m$1CASE_NAME\033[0m pe_mask=$PE_MASK"
    else
        RESULT_MSG+=(" \033[33m$CASE_NAME\033[0m pe_mask=$2 \033[32m[PASS]\033[0m")
        echo -e "\033[32m[[PASS]] \033[33m$CASE_NAME\033[0m pe_mask=$PE_MASK"
    fi
    return $rc
}

# $1=image name.
function traversing_case() {
    for PE_MASK in {1..15}; do
        exeucte_case $1 $PE_MASK
        rc=$?
        if [ $rc -ne 0 ]; then
            return $PE_MASK
        fi
    done
    return 0
}

# $1=pe mask..
function traversing_all_cases() {
    MSG_DISPLAY=" 2>&1 > /dev/null"
    CASE_LIST="${CURDIR}/image_list.log"
    if [ ! -f "${CASE_LIST}" ]; then
        error "${CASE_LIST} not exist!"
        exit 1
    fi
    info "Traversing all cases:"
    PASS_NUM=0
    FAIL_NUM=0
    SKIP_NUM=0
    CASE_NUM=$(wc -l < ${CASE_LIST})
    SKIP_LIST=("bu_plic" "bu_uart" "bu_pvt" "bu_cali_flow" "bu_power_mgr" "bu_hif_msix_forward")
    INDEX_=1
    while IFS= read -r line
    do
        CASE_NAME=$(basename "$line")
        if echo "${SKIP_LIST[@]}" | grep -qw "$CASE_NAME"; then
            warning "($INDEX_/$CASE_NUM) $CASE_NAME !SKIP!"
            SKIP_NUM=$((SKIP_NUM + 1))
        else
            info "($INDEX_/$CASE_NUM) $CASE_NAME"
            exeucte_case ${CASE_NAME} $1
            rc=$?
            if [ $rc -eq 0 ];then
                PASS_NUM=$((PASS_NUM + 1))
            else
                FAIL_NUM=$((FAIL_NUM + 1))
                # break
            fi
        fi
        INDEX_=$((INDEX_ + 1))
    done < ${CASE_LIST}

    print_case_results
    echo -e "\033[1m\033[32mPASS:${PASS_NUM}/${CASE_NUM}, \033[31mFAIL:${FAIL_NUM}/${CASE_NUM},  \033[33mSKIP:${SKIP_NUM}/${CASE_NUM}. \033[0m"
}

# __main__
if [[ $# -eq 0 || $1 == '-h' ]]; then
    help_menu
else
    if [[ -f $1 ]]; then
        AURORA_EIC_TEST=$1
    elif [[ -f "$1/$EIC_TEST" ]]; then
        AURORA_EIC_TEST=$1/$EIC_TEST
    else
        error "$EIC_TEST not found"
        exit 1
    fi
    if [[ $# -eq 1 ]]; then
        info "traversing_all_cases() pe_mask=15"
        traversing_all_cases 15
    elif [[ $# -eq 2 ]]; then
        if isdigit $2; then #$1=pe_mask
            info "traversing_all_cases() pe_mask=$2"
            traversing_all_cases $2
        else #$1=case_name
            info "execute_case($1) pe_mask={1...15}"
            traversing_case $2
        fi
    elif [[ $# -eq 3 ]]; then
        if isdigit $2; then #$2=pe_mask
            info "exeucte_case($3) pe_mask=$2"
            exeucte_case $3 $2
        elif isdigit $3; then #$3=pe_mask
            info "exeucte_case($2) pe_mask=$3"
            exeucte_case $2 $3
        else
            help_menu
        fi
    else
        help_menu
    fi
fi

exit $?
