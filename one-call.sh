#!/bin/bash

source .env

############### Delete Mariadb Service If Exist ##################
if [ -z "${MARIADB_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=mariadb`
else
    CONTAINER_ID=`docker ps -aq -f name=${MARIADB_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Mariadb Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

############### Delete Adminer Service Container If Exist ##################
if [ -z "${ADMINER_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=adminer`
else
    CONTAINER_ID=`docker ps -aq -f name=${ADMINER_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Adminer Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi


############### Delete Redis Service Container If Exist ##################
if [ -z "${REDIS_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=redis`
else
    CONTAINER_ID=`docker ps -aq -f name=${REDIS_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Redis Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

############### Delete Redis-Commander Service Container If Exist ##################
if [ -z "${REDIS_COMMANDER_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=redis-commander`
else
    CONTAINER_ID=`docker ps -aq -f name=${REDIS_COMMANDER_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Redis-commander Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

############### Delete Traefik Service Container If Exist ##################
if [ -z "${TRAEFIK_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=traefik`
else
    CONTAINER_ID=`docker ps -aq -f name=${TRAEFIK_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Traefik Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

############### Delete Account Service Container If Exist ##################
if [ -z "${ACCOUNT_SERVICE_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=account-service`
else
    CONTAINER_ID=`docker ps -aq -f name=${ACCOUNT_SERVICE_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Account Service Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

############### Delete Enterprise Service Container If Exist ##################
if [ -z "${ENTERPRISE_SERVICE_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=enterprise-service`
else
    CONTAINER_ID=`docker ps -aq -f name=${ENTERPRISE_SERVICE_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Enterprise Service Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

############### Delete Report Service Container If Exist ##################
if [ -z "${REPORT_SERVICE_CONTAINER_NAME}" ]; then
    CONTAINER_ID=`docker ps -aq -f name=report-service`
else
    CONTAINER_ID=`docker ps -aq -f name=${REPORT_SERVICE_CONTAINER_NAME}`
fi
if [[ ${CONTAINER_ID} != "" ]]; then
    printf "Remove Report Service Container With ID = ${CONTAINER_ID}\n"
    docker rm -f ${CONTAINER_ID}
fi

###################################################################
########### Create Mariadb, Adminer, Redis, ####################### 
########### Redis-Commander, Traefik, Account-Service, ############
########### Enterprise-Service Container  #########################
###################################################################

VAR=`docker network inspect ${SERVICES_NETWORK}`
NETWORK_EXIST=$?
if [[ ${NETWORK_EXIST} != 0 ]]; then
    printf "Create Network ${SERVICES_NETWORK}\n"
    docker network create -d bridge ${SERVICES_NETWORK}
fi
docker-compose up -d
cd python-scripts
python -m pip install -r requirements.txt
python dump_facedata_db.py
python consumer_to_db.py


