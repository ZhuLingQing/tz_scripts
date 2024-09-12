#!/bin/bash
#$1: dest_ip

if [ $# -ne 1 ]; then
    echo "Usage: $0 dest_ip"
    exit 1
fi
SRC_PATH="build_aurora_mcp/ports/rt_mcp/aurora_mcp.bin"
FILE_NAME=$(basename $SRC_PATH)

SRC_BASE_PATH=/nfs/homes/tzhu/projects/pace2/gf_aurora/
DST_BASE_PATH=/home/ubuntu/tzhu/images
TEMP_LOCAL_PATH=/u/tzhu/.temp/

SRC_HOST_NAME=tzhu-ubuntu2
SRC_USER_NAME=tzhu
SRC_PASSWORD=Bianshao.1221

IP_PREFIX=10.102.16
DST_HOST_NAME=$IP_PREFIX.$1
DST_USER_NAME=ubuntu
DST_PASSWORD=test1234

#$1: relative path of source
function copy_from_source() {
    src_dir=$SRC_BASE_PATH$1
    dest_dir=$TEMP_LOCAL_PATH
    host=$SRC_HOST_NAME
    port=22
    username=$SRC_USER_NAME
    password=$SRC_PASSWORD
    
    ./scp2local.expect $host $port $username $password $src_dir $dest_dir
    return $?
}

#$1: relative path of local
function copy_to_target() {
    src_dir=$TEMP_LOCAL_PATH$1
    dest_dir=$DST_BASE_PATH
    host=$DST_HOST_NAME
    port=22
    username=$DST_USER_NAME
    password=$DST_PASSWORD
    
	#echo "copyt to bu machine from '$src_dir' to '$dest_dir'"

    ./scp2remote.expect $host $port $username $password $src_dir $dest_dir
    return $?
}

echo "#1. clean local temp file"
rm -f $TEMP_LOCAL_PATH$FILE_NAME

echo "#2. copy from $SRC_HOST_NAME"
copy_from_source $SRC_PATH
#scp -r tzhu@tzhu-ubuntu2:$SRC_BASE_PATH$SRC_PATH $TEMP_LOCAL_PATH
if [ $? -ne 0 ]; then
    echo "copy from $SRC_HOST_NAME failed"
    return 1
fi

#echo "    print file hash"
find $TEMP_LOCAL_PATH -name $FILE_NAME | xargs md5sum

echo "#2. start copy to $DST_HOST_NAME "
copy_to_target $FILE_NAME
#scp -r $TEMP_LOCAL_PATH$FILE_NAME ubuntu@$DEST_IP:$DST_BASE_PATH
if [ $? -ne 0 ]; then
    echo "copy to $DST_HOST_NAME failed"
    return 1
fi

echo "copy done."
return 0
