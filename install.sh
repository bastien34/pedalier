echo 'ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="e026", MODE="660", GROUP="plugdev", SYMLINK+="QinHeng Electronics"' >> /etc/udev/rules.d/51-pedalier-permissions.rules
echo 'SUBSYSTEM=="input", KERNEL=="event*", MODE="0660", OPTIONS+="last_rule"' >> /etc/udev/rules.d/51-pedalier-permissions.rules
udevadm control --reload-rules

# adduser username plugdev