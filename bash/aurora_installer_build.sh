#!/bin/bash
CURDIR=$(cd "$(dirname $0)";pwd)

set -e

if [[ $# -eq 1 ]] && [[ $1 == "-h" ]]; then
  echo "Usage: installer_build.sh [GF_AURORA_DIR]"
  exit 1
elif [[ $# -eq 1 ]]; then
  GF_AURORA_DIR=$1
else
  echo "Usage: installer_build.sh [GF_AURORA_DIR]"
  exit 1
fi

# Set the script name
SCRIPT_NAME="install_firmware.sh"

# Set the destination directory
DEST_DIR="${CURDIR}/../../build_runtime/gf_aurora_archive"
if [ ! -d ${DEST_DIR} ]; then mkdir -p ${DEST_DIR}; fi

# Set the archive name
if [ -n "$VERSION" ]; then
  FW_VERSION=${VERSION}
else
  FW_VERSION=$(git rev-parse --short=8 HEAD)
fi
ARCHIVE_NAME="photonera_firmware_aurora_$FW_VERSION.run"

#remove the current run file image
rm -f photonera_firmware_aurora_*.run

# Make sure the destination directory exists
MCP_TARGET_DIR=${DEST_DIR}/mcp_binary/
MCP_SOURCE_PATH=${CURDIR}/../../build_aurora_mcp/ports/rt_mcp/aurora_mcp.bin
if [ ! -f ${MCP_SOURCE_PATH} ]; then
  make mcp -j
  if [ ! -f ${MCP_SOURCE_PATH} ]; then
    echo "fail to build runtime mcp"
    exit 1
  fi
fi
mkdir -p ${MCP_TARGET_DIR}
cp ${MCP_SOURCE_PATH} ${MCP_TARGET_DIR}

# Make sure the destination directory exists
mkdir -p "${DEST_DIR}/data/"

cp -rf ${GF_AURORA_DIR}/* "${DEST_DIR}/data/" 
cp ${CURDIR}/install.sh "${DEST_DIR}/${SCRIPT_NAME}"

# Create the archive
makeself  ${DEST_DIR} \
         "${ARCHIVE_NAME}" \
         "Installation script and files" \
         ./${SCRIPT_NAME}

rm -rf ${DEST_DIR}
