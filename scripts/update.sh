#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE}" )" &> /dev/null && pwd )"
if [ "$EUID" -ne 0 ]
	then echo "Trying to run as root"
	sudo "$SCRIPT_DIR/update.sh"
	exit
fi
if [ -f Dockerfile ]
	then echo "Dockerfile exists, continuing..."
else
	echo "Dockerfile does not exist, please run this script in the same directory as the Dockerfile, or make sure the Dockerfile exists. You can use the example in the repository."
	exit
fi
DOCKER_CONTAINER_EXISTS=$(sudo docker ps -a --format '{{.Names}}' | grep -wq "agb" && echo true || echo false)
if [ $DOCKER_CONTAINER_EXISTS = true ]
	then echo Make sure you have ran /backup and /shutdown if the bot is running, you have 5 seconds to CTRL-C
	sleep 5s
fi
echo Building Docker image...

sudo docker build -t trwy7/agb .
if [ $DOCKER_CONTAINER_EXISTS = true ]
	then sudo docker stop agb
	sudo docker remove agb
fi
"$SCRIPT_DIR/start.sh"
echo "Update complete"