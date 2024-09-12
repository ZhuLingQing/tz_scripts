#!/usr/bin/env bash
set -e

# Set the destination directory
DEST_DIR="/opt/photonera/firmware/aurora"
DEST_MCP_DIR="/lib/firmware/lgt"

# Create the destination directory
if [[ -d "$DEST_DIR" ]]; then
  rm -rf $DEST_DIR/*
  echo "Uninstall previous installed firmware version $DEST_DIR/*"
else
  mkdir -p "$DEST_DIR"
fi
if [[ -f "$DEST_MCP_DIR/aurora_mcp.bin" ]]; then
  rm -f $DEST_MCP_DIR/aurora_mcp.bin
  echo "Uninstall previous installed firmware image $DEST_MCP_DIR/aurora_mcp.bin"
elif [[ ! -d "$DEST_MCP_DIR" ]]; then
  mkdir -p "$DEST_MCP_DIR"
fi

# Extract the contents of the makeself archive
echo "Extracting files..."
cp -rf ./data/* "$DEST_DIR"
chmod -R 755  "$DEST_DIR/../../../"

echo "Extracting mcp image"
cp ./mcp_binary/aurora_mcp.bin ${DEST_MCP_DIR}
chmod -R 755  "$DEST_MCP_DIR/"
# Perform your installation steps here

# Example: Copy files to a system directory
# cp -r "$DEST_DIR"/* /usr/local/bin/

echo "Installation aurora firmware complete."

# Clean up the temporary installation files if needed
# rm -rf "$DEST_DIR"

exit 0
