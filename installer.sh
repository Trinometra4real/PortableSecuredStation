#!/bin/bash
echo "Starting"
pytest="$(python3 -V 2> /dev/null)"
gittest="$(git -v 2> /dev/null)"
echo "args: $0"
if [ -z "$pytest" ]
then
    sudo apt -y install python3 pip
fi

if [ -z "$gittest" ]
then
    sudo apt -y install git
fi

if [[ "$1" == *local* ]]
then
    echo "Installing in local user";
    git clone https://github.com/Trinometra4real/PortableSecuredStation.git /tmp/PSS
    cp -r "/tmp/PSS/App" "/home/$USER/.local/lib/PSS"
    cp "/tmp/PSS/pss" "/home/$USER/.local/bin/"
    cp -r "/tmp/PSS/USB" "/home/$USER/.config/PSS"
    rm -rf /tmp/PSS


elif [[ "$1" == *remove* ]]
then
    if [[ "$2" == *local* ]]
    then
        rm -rf /home/$USER/.local/lib/PSS
        rm -f /home/$USER/.local/bin/pss
        rm -rf /home/$USER/.config/PSS
        echo "Uninstall done"
    elif [[ "$2" == *global* ]]
    then
        sudo rm -rf /usr/lib/PSS
        sudo rm -rf /var/lib/PSS
        sudo rm -f /usr/local/bin/pss
        sudo groupdel PssUser
        echo "Uninstall done"
    fi
else
    echo "Installing for all users";
    git clone https://github.com/Trinometra4real/PortableSecuredStation.git /tmp/PSS;
    echo "Unpacking /usr/lib/PSS"
    sudo cp -r "/tmp/PSS/App" "/usr/lib/PSS"
    
    sudo cp "/tmp/PSS/pss" "/usr/local/bin/"
    echo "Unpacking /var/lib/PSS"
    sudo cp -r "/tmp/PSS/USB" "/var/lib/PSS"
    echo "installed command pss"
    sudo groupadd PssUser
    echo "Group PssUser added"
    echo "Applying settings"
    sudo chmod -R 750 /var/lib/PSS
    sudo chmod -R 750 /usr/lib/PSS
    sudo chmod 4750 /usr/local/bin/pss

    sudo chown root:PssUser /usr/local/bin/pss
    sudo chown -R root:PssUser /usr/lib/PSS
    sudo chown -R root:PssUser /var/lib/PSS

    echo "Cleaning ..."

    rm -rf /tmp/PSS

    sudo apt -y update
    sudo apt -y upgrade
    sudo apt -y install python3
    sudo apt -y install pip
    echo "installing required packages ..."
    pip install pycryptodome --break-system-package;
    echo "Installation done."
fi
