# smashbox-docker
This repository contains dockerfiles and scripts to easily deploy CERNBox client-testing configurations with smashbox framework.

## Usage
```
docker build -t debian-smashbox 
docker run -it -e SMASHBOX_OC_ACCOUNT_NAME="XXXX" -e  SMASHBOX_OC_ACCOUNT_PASSWORD="YYYYYY" -e SMASHBOX_OC_SERVER="cernbox.cern.ch" debian-smashbox:latest bash
```
## Environment variables
```
  SMASHBOX_OS 
  SMASHBOX_CLIENT_VERSION
  SMASHBOX_OC_SERVER
  SMASHBOX_OC_ACCOUNT_NAME
  SMASHBOX_OC_ACCOUNT_PASSWORD
  SMASHBOX_TESTDIR
  SMASHBOX_SSL_ENABLED
```
