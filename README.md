Network-Layer Ids


- Installations

`sudo docker build -t ids:1.1 .`

`sudo docker run --network=host --privileged=true -d ids:1.1 tail -f /dev/null`

`sudo docker exec -it (container-id) /flowmeter/run.sh`