# LevelAPI


## Docker
A dockerfile is provided, ready for building.
To build the image:
Clone this repository
Move to the LevelAPI folder
Run this command:  docker build -t levelapi .
CHeck with the command: docker images
If you want to run the docker locally, start docker gui or  run this command:
docker run -p 8080:8080 --restart OnFailure --name coffeedocker levelapi
The left port is external access point, the right is the internal port used by the API

To push the docker to the example azure container:
Make sure the docker is built.
Find your azure conataier registry login server address ( <YOURSERVER>.azurecr.io )
Login to the server:
docker login <YOURSERVER>.azurecr.io
Tag/select the image you want to push to azure
docker tag levelapi <YOURSERVER>.azurecr.io/levelapi
Finally push to azure:
docker push coffeefinderregistry.azurecr.io/levelapi

## Azure
Create a new Container instance in azure portal.
Select the container registry you created earlier, thats linked to the docker.
If you got the "az"  azure CLI run to show the container status:
az container show --resource-group <YourResourceGroup --name <YourContainerInstacneName> --output table
for more info, 
az container show --resource-group <YourResourceGroup --name <YourContainerInstacneName> 
