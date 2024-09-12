if [ $# -lt 2 ]; then
	echo 'arg1: author, arg2: path'
	exit 1
fi
author="$1"
pushd $2
today=`date +"%Y-%m-%d"`
ago=`date +"%Y-%m-%d" -d "-365 days"`
git log --author="${author}" --since="${ago}" --until="${today}" --pretty=tformat: --numstat | gawk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "add: %s del: %s total add: %s lines.\n", add ,subs, loc }' -
popd
