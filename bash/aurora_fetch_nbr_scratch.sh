#!/bin/bash

function info() {
    local yellow="33m"
    echo -e "\033[${yellow}$* \033[0m" 2>&1
}

#list pcie info
function get_reg_bar() {
	REG_BAR_STR=`lspci -vvv -nn -d 060e: | grep "Region 2"`
	# echo $REG_BAR_STR
	IFS=' ' read -r -a REG_BAR_ARRAY <<< "$REG_BAR_STR"
	STR_NUM=${#REG_BAR_ARRAY[@]}
	# echo "Splite to $STR_NUM"
	if [ $STR_NUM -gt 4 ]; then
		echo ${REG_BAR_ARRAY[4]}
	else
		echo "reg bar not found."
		exit 1
	fi
}

((reg_bar_base=0x$(get_reg_bar)))
((nbr_base=0x2600000))
((reg_offset=0x8))
((pe_offset=0x2000000))

cpu_array=("MCP" "PE0" "PE1" "PE2" "PE3")
reg_array=("scratch   " "AID       " "sketchpad0" "sketchpad1" "sketchpad2" "sketchpad3")

if [ $# -eq 1 ] && [ $1 == "-c" ]; then
	info "clear nbr-scratch"
	for ((i=0;i<${#cpu_array[*]};i++)); do
		for ((j=0;j<${#reg_array[*]};j++)); do
			if [ $j -eq 1 ]; then continue; fi
			((reg_addr=${reg_bar_base}+${nbr_base}+${pe_offset}*${i}+${reg_offset}*${j}))
			fmt_reg=`awk -v c=${reg_addr} 'BEGIN { printf "%X", c;}'`
			str_mem=`./lgtmem 0x$fmt_reg q 0`
		done
	done
else
	info "fetch nbr-scratch"
	for ((i=0;i<${#cpu_array[*]};i++)); do
		echo "This is ${cpu_array[i]}"
		for ((j=0;j<${#reg_array[*]};j++)); do
			if [ $j -eq 1 ]; then continue; fi
			((reg_addr=${reg_bar_base}+${nbr_base}+${pe_offset}*${i}+${reg_offset}*${j}))
			fmt_reg=`awk -v c=${reg_addr} 'BEGIN { printf "%X", c;}'`
			str_mem=`./lgtmem 0x$fmt_reg q`
			reg_va=${str_mem##*x}
			echo "${reg_array[j]}: 0x$fmt_reg = 0x${reg_va}"
		done
	done
fi

