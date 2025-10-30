PATH="/home/dgourland/GIT/PortableSecuredStation/TESTS/storage_disk.img"
DEST="/home/dgourland/GIT/PortableSecuredStation/TESTS/VHD"

sudo dd if=/dev/zero of=$PATH/virtual_disk.img bs=1G count=1  # bs = block size, count = number of blocks
sudo mkfs -t ext4 $PATH/virtual_disk.img # sudo mkfs -t <file_system_type> <virtual hard disk>
mkdir $DEST
sudo mount -o loop $PATH/virtual_disk.img $DEST # mount virtual disk to target destination
