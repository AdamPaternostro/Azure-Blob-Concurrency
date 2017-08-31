#----------------------------------------------------------------------------------\
# For Windows 10 64 install (install python via website)
# add to path: C:\Users\adpater\AppData\Local\Programs\Python\Python36-32
# add to path: C:\Users\adpater\AppData\Local\Programs\Python\Python36-32\Scripts
# download get-pip.py
# python get-pip.py
# pip install azure
# python -m pip install -U pip
# https://github.com/Azure-Samples/storage-blob-python-getting-started
# docker build -t blobconcurrency .
# docker run blobconcurrency python3 /app/BlobConcurrency.py 1mb.txt {parmeter: 1mb.txt, 15mb.txt, 40mb.txt, 80mb.txt, 150mb.txt, 400mb.txt}
# docker login
# docker tag blobconcurrency adampaternostro/blobconcurrency:latest
# docker push adampaternostro/blobconcurrency:latest
#----------------------------------------------------------------------------------
import os
import datetime
import sys

from azure.storage.table import TableService, Entity
from azure.storage.blob import BlockBlobService

# Print command line
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

# Provide a default if no command line
fileToDownload="1mb.txt"

# Override file name if command line is passed in
if (len(sys.argv)  == 2) : 
    fileToDownload=sys.argv[1]
    print("Using command line parameters:",sys.argv[1])

print("fileToDownload:",fileToDownload)

# Blob
ACCOUNT_NAME = "<<REMOVED>>"
ACCOUNT_KEY = "<<REMOVED>>"
CONTAINER_NAME = "concurrencytest"

# Connect to Azure services
block_blob_service = BlockBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
table_service = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
table_service.create_table('timingtable')

# Run for a certain amount of time (5 minutes for 300 seconds)
endLoop = datetime.datetime.now() + datetime.timedelta(seconds=300)
while datetime.datetime.now() < endLoop:
    # Create a unique file name to avoid collisions
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    blobTempName = datetime.datetime.now().strftime("%m-%d-%y-%H-%M-%S-%f.txt")
    print("blobTempName",blobTempName)

    # Download blob and capture timing
    startTime = datetime.datetime.now()
    block_blob_service.get_blob_to_path(CONTAINER_NAME, fileToDownload, blobTempName)
    stopTime = datetime.datetime.now()

    elapsedTime = stopTime - startTime
    print("elapsedTime:", elapsedTime.total_seconds())

    # Delete the blob to save on storage
    os.remove(blobTempName)

    # Save the timing to an Azure Storage Table
    task = {'PartitionKey': 'Timing', 'RowKey': blobTempName, 'fileName' : fileToDownload, 'elapsedTime' : elapsedTime.total_seconds(), 'stateTime': startTime.strftime("%m-%d-%y-%H-%M-%S-%f"), 'stopTime': stopTime.strftime("%m-%d-%y-%H-%M-%S-%f")}
    table_service.insert_entity('timingtable', task)

