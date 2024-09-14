#!/bin/bash
 
while true; do
    # Rescan PCI bus
    echo 1 > /sys/bus/pci/rescan
    echo "scan pcie" 
    # Check for devices with class code 060e
    if lspci -nn | grep -q '\[060e:2100\]'; then
        echo "Detected PCIe device with class code 060e, exiting."
        break
    fi
 
    # Wait for 1 second before the next iteration
    sleep 1
done