
cur_dir=$(cd "$(dirname $0)";pwd)

trap 'echo "test quit"; stty echo; bash ${cur_dir}/kill_qemu.sh; exit 1' INT

rm /u/tzhu/projects/pace2/gordian/log -rf
rm *.log -f
clear

KVM_MODE_LS=`ls /dev/kvm -l`
KVM_MODE=($KVM_MODE_LS)
if [ ${KVM_MODE[0]} != "crwxrw-rwx+" ]; then
	sudo chmod 777  /dev/kvm
fi

qemu_img=/u/tzhu/Downloads/u1804-server.qcow2
echo "launch:qemu image is $qemu_img"

/u/tzhu/projects/pace2/qemu/build/qemu-system-x86_64 -enable-kvm -m 20480 -nographic -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::9527-:22 -drive file=$qemu_img,media=disk,if=virtio -device pci-lt-dev -cpu qemu64,pdpe1gb -smp 4 > /dev/null &
sleep 2
if [[ $# -eq 1 ]] && [[ $1 == "log" ]]; then
	LOG_EN=t
	SEMIH_EN=t
else
	LOG_EN=f
	SEMIH_EN=f
fi

echo "launch:gordian"
pushd /u/tzhu/projects/pace2/gordian
#./funcsim_lin sel [qemu] >log_qemu.log 2>&1
./funcsim_lin sel [qemu] ft_test t no_shell t semihosting $SEMIH_EN log $LOG_EN |tee $cur_dir/gordian.log 
popd

stty echo
echo "test exit"
exit 0
