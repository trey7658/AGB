#!/bin/bash
if [ "$EUID" -ne 0 ]
	then echo "Trying to run as root"
	sudo ./update.sh
	exit
fi
if [ -f Dockerfile ]
	then echo "Dockerfile exists, continuing..."
else
	echo "Dockerfile does not exist, please run this script in the same directory as the Dockerfile, or make sure the Dockerfile exists. You can use the example in the repository."
	exit
fi
git stage *
echo Make sure you have ran /backup and /shutdown if the bot is running, you have 5 seconds to CTRL-C
sleep 5s
read -p "Commit message: " commit
git commit -m "$commit"
sudo docker build -t trwy7/agb .
sudo docker stop agb
sudo docker remove agb
./start.sh
