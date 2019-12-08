#!/bin/sh
echo ""
echo "#########################################################################"
echo "This script runs MQTT broker on the computer."
echo "All arguments passed to the script are propagated to docker."
echo "If you want to run the broker in the background, specify argument \"-d\"."
echo "#########################################################################"
echo ""

if [ "$(command -v docker)" == "" ]; then
        echo "This script requires docker to be present"
        echo "on the computer. Please install docker."
fi

# Run mosquitto container with port 1883 (non-TLS)
# published to host network interface and
# delete the container after the execution has finished
docker run --rm --name testbroker -p 1883:1883 "$@" eclipse-mosquitto
