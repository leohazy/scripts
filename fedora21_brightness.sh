 #!/bin/bash
cd /boot/grub2
cp grub.cfg grub.cfg1
sed -i 's/quiet/quiet video.use_native_backlight=1 acpi_osi=linux/' grub.cfg
exit
Fedora20
cd /boot/grub2
cp grub.cfg grub.cfg1
sed -i 's/quiet/quiet acpi_backlight=vendor acpi_osi=linux/' grub.cfg
exit