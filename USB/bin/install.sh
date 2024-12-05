apt -y update
apt -y full-upgrade
apt -y install python3 git postgresql postgresql-contrib default-jre gnupg
mkdir /etc/SafeDataTransfert
cp configFiles/postgresql.conf /etc/postgres/14/main
cp configFiles/pg_hba.conf /etc/postgres/14/main
cp systemd/* /etc/systemd/system
mkdir /Setup
git clone https://github.com/sassoftware/python-keyutils.git /Setup/keyutils
pip install --upgrade pip --break-system-package
pip install gnupg --break-system-package
pip install requests --break-system-package
cp UserManager.py /Setup
cp localServer.py /Setup
apt -y update
apt -y upgrade
apt -y autoremove
