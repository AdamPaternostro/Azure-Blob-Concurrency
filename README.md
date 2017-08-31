
# Azure-Blob-Concurrency
Docker container that runs on Azure blob using Alpine Linux with Azure Python SDK to put a load on Azure Storage to see the download times.  The timings are saved to an Azure Storage Table.  It is up to you to download and analyze.

### To Run this code
1. Create an Azure Storage Account
2. Create an Azure Batch Account 
3. Create some different sized blobs and place in your storage account
4. Test the Python code locally
5. Build the Docker image
6. Upload image to a repository
7. Edit the Shipward config files
8. Issue the below commands to run the process

### Get Shipyard Docker image, Create the Batch Pool, Run the Job, Delete the Pool
```
sudo docker pull alfpark/batch-shipyard:cli-latest

sudo docker run --rm -it -v /home/shipyarduser/pythonblob:/configs -e SHIPYARD_CONFIGDIR=/configs alfpark/batch-shipyard:cli-latest pool add

sudo docker run --rm -it -v /home/shipyarduser/pythonblob:/configs -e SHIPYARD_CONFIGDIR=/configs alfpark/batch-shipyard:cli-latest jobs add --tail stdout.txt

sudo docker run --rm -it -v /home/shipyarduser/pythonblob:/configs -e SHIPYARD_CONFIGDIR=/configs alfpark/batch-shipyard:cli-latest pool del
```
