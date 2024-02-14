#!/bin/bash
# This script is used to install AGB in docker, this script should install dependencies and start the bot.
# This script should be run in the same directory as the Dockerfile
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE}" )" &> /dev/null && pwd )"
if [ "$EUID" -ne 0 ]
	then echo "This script should be run as root. Please enter your password when propmted."
	sudo bash "$SCRIPT_DIR/install.sh"
	exit
else
    echo This is the AGB install script, you can find the source code at https://github.com/trwy7/agb
fi
read -n 1 -s -r -p "Press any key to continue, or q to quit"
if [[ $REPLY =~ ^[Qq]$ ]]
    then exit
fi
clear
echo Checking for APT
if [ -x "$(command -v apt)" ]
    then echo "APT exists, continuing..."
else
    echo "APT does not exist, please run this script on a Debian based system."
    exit
fi
echo "This script will install docker and git, agb will be installed to a docker container."
read -n 1 -s -r -p "Press any key to continue, or q to quit"
if [[ $REPLY =~ ^[Qq]$ ]]
    then exit
fi
clear
echo Installing dependencies...
sudo apt update
sudo apt install -y docker.io
sudo apt install -y git
read -n 1 -s -r -p "Are you planning on developing? (y/n)"
if [[ $REPLY =~ ^[Yy]$ ]]
    then echo Installing python and dependencies...
    sudo apt install python3 python3-pip
    pip install -r requirements.txt
fi
if [ -d $SCRIPT_DIR/../.git ]
    then cd $SCRIPT_DIR/..
else
    git clone https://github.com/trwy7/agb.git agb
fi

if [ -f Dockerfile ]
    then echo "Dockerfile exists, continuing..."
elif [ -f Dockerfile\ example ]
    then echo "Dockerfile does not exist, using default Dockerfile"
    cp "Dockerfile example" "Dockerfile"
    exit
else 
    echo Attempting git clone...
    git clone https://github.com/trwy7/agb.git agb
    cd agb

fi

"$SCRIPT_DIR/update.sh"