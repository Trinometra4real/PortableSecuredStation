# PortableSecuredStation
A simple Portable Secured Station to store secret data into a self manage encrypted storage system

*Warning: Unsecure Repository*

**Non-Root User installation**

*Systemd*
systemd path: /home/$USER/.config/systemd/user
export XDG_RUNTIME_DIR=/run/user/$UID
systemctl --user [ARGS]

*PATH (Perms: 700) *
 - /home/$USER/.local/bin/ -> executables
 - /home/$USER/.local/lib/ -> dépendences / fichier liés à l'executable
 - /home/$USER/.local/share/ -> doc / ressources /
 - /tmp -> fichiers temporaires à détruire après utilisation (privilégier le /run/tmpfs)
 - /home/$USER/.config/$APP/ -> fichiers de configuration de l'application

**Root User Installation (All user on the machine)**

*Group Setup (if restricted access needed)*
sudo groupadd $groupname
sudo usermod -aG $groupname $USER
sudo chown -R root:$groupname $APP_PATH

*PATH*
 - /usr/local/bin/cmd-line -> Perm 750: executable (Exec point)
 - /usr/lib/$APP -> Perm 750: direct dependencies for executable (enable root access for update (root:$groupname Perm: 4755 or 4750))
 - /var/lib/$APP -> Perm 760: data stored by the application
 - /etc/$APP -> Perm 760: config files for the application

*tmpfs*

sudo mount -t tmpfs -o size=10M tmpfs /mnt/mytmpfs -> permet de monter le tmpfs dans un répertoire pour un stockage de 10 méga
