FROM alpine

# For Python 3
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache

# For Azure storage (mainly the cryptography build process)
# https://cryptography.io/en/latest/installation/
RUN apk add --update make cmake gcc g++ gfortran && \
    apk add python3-dev && \
    apk add libffi-dev && \
    apk add openssl-dev

# Azure storage for Python
COPY requirements.txt /tmp/requirements.txt 
RUN pip install -r /tmp/requirements.txt

# Python code    
WORKDIR /app
ADD BlobConcurrency.py /app

# Comment out for Shipyard
# ENTRYPOINT ["python3","./BlobConcurrency.py"]
# CMD ["1mb.txt"]

