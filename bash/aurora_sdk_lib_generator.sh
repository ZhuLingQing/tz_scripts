#!/usr/bin/env bash
CURDIR=$(cd "$(dirname $0)";pwd)
set -e

if [[ $# -eq 1 ]] && [[ $1 == "-h" ]]; then
    echo "Usage: aurora_lib.sh [AURORA_LIB_DIR]"
    exit 1
elif [[ $# -eq 1 ]]; then
    AURORA_LIB_DIR=$1
else
    echo "Usage: aurora_lib.sh [AURORA_LIB_DIR]"
    exit 1
fi

if [ ! -d ${AURORA_LIB_DIR}/lib ] ; then
    echo "${AURORA_LIB_DIR}/lib is not exist"
    exit 1
fi

GF_AURORA_DIR=${CURDIR}/../..
CROSS_AR="/nfs/swg/lt-compiler/lt-latest-release/bin/riscv64-unknown-elf-ar"
#copy ${AURORA_LIB_DIR}/include/third_party
if [ ! -d ${AURORA_LIB_DIR}/include/third_party ] ; then
    mkdir -p ${AURORA_LIB_DIR}/include/third_party
fi
cp ${GF_AURORA_DIR}/build_runtime/_deps/protothreads-src/*.h ${AURORA_LIB_DIR}/include/third_party
cp ${GF_AURORA_DIR}/build_runtime/_deps/erpc-src/erpc_c/infra/erpc_version.h ${AURORA_LIB_DIR}/include/third_party/
#create ${AURORA_LIB_DIR}/lib
num_a=`find ${AURORA_LIB_DIR}/lib -name "lib*.a"| wc -l`
echo "Find ${num_a} lib*.a"
find ${AURORA_LIB_DIR}/lib -name "lib*.a"|xargs -L 1 ${CROSS_AR} x
${CROSS_AR} rcs libauroradev.a ./*.obj
rm ./*.obj
rm ${AURORA_LIB_DIR}/lib/lib*.a
mv ./libauroradev.a ${AURORA_LIB_DIR}/lib
cp ${GF_AURORA_DIR}/samples/cmake/CMakeLists.txt ${AURORA_LIB_DIR}/lib
cp ${GF_AURORA_DIR}/ports/rt_pe/rt_pe.cpp ${AURORA_LIB_DIR}/lib/main.cpp
cp ${GF_AURORA_DIR}/samples/cmake/riscv.cmake ${AURORA_LIB_DIR}/lib
#create ${AURORA_LIB_DIR}/bin
if [ ! -d ${AURORA_LIB_DIR}/bin ] ; then
    mkdir ${AURORA_LIB_DIR}/bin
fi
cp ${GF_AURORA_DIR}/samples/cmake/ltclcc.sh ${AURORA_LIB_DIR}/bin



