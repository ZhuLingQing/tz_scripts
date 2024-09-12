#!/bin/bash
warning() { echo -e "\e[33m$*\e[0m"; }
pass() { echo -e "\e[32m$*\e[0m"; }
fail() { echo -e "\e[31m$*\e[0m"; }

cur_dir=$(cd "$(dirname $0)";pwd)
gf_path=/u/tzhu/projects/pace2/gf_aurora
bin_path=/u/tzhu/projects/pace2/binary
mcp_path=$gf_path/build_aurora_mcp/ports/rt_mcp
rt_pe=$gf_path/build_aurora_pe/ports/rt_pe/rt_pe.bin
#rt_pe=/u/tzhu/.cache/ising.bc.bin
tar_pe=$bin_path/sample/swd_cmd/swd_cmd40.bin

if [ ! -f "$mcp_path/aurora_mcp.bin" ]; then
    red "    MCP not exist."
	exit 1
fi

md5sum $mcp_path/aurora_mcp.bin
${cur_dir}/aurora_eic_test --gtest_filter=FirmwareTest.DirectLoadMcpFirmware --mcp_fw_path=$mcp_path
rc=$?
if [ $((rc)) -ne 0 ]; then
	fail "fail to LoadMcp ${rc}"
elif [ $# -eq 1 ] && [ $1 == "pe" ]; then
	if [ ! -f "$rt_pe" ]; then
		warning "    PE not exist. Directly load."
	else
		echo "reload PE firmware"
		rc=`cp $rt_pe $tar_pe`
		if [ $((rc)) -ne 0 ]; then
			fail "fail to copy rt_pe ${rc}"
			exit 1
		fi
	fi
	if [ ! -f "$tar_pe" ]; then
		fail "No pe at $tar_pe"
		exit 1
	fi
	md5sum $tar_pe
	${cur_dir}/aurora_eic_test --gtest_filter=CommandTest.SoftDefineLoadFirmware --pe_mask=15
	rc=$?
	if [ $((rc)) -ne 0 ]; then
		fail "fail to DownloadPE ${rc}"
	fi
fi

if [ $((rc)) -ne 0 ]; then
	fail "[#FAIL#] \e[0m $rc"
else
	pass "[#PASS#]"
fi
exit $((rc))
