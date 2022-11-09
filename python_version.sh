#!/bin/bash

PYTHON_VERSION='python'
FIRST_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[0])'`
VERSION_EXIST=$?
if [[ $VERSION_EXIST == 0 && $FIRST_VERSION -ge 3 ]]; then
    SECOND_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[1])'`
    if [[ $SECOND_VERSION -lt 8 ]]; then
        PYTHON_VERSION='python3'
        SECOND_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[1])'`
        VERSION_EXIST=$?
        if [[ $VERSION_EXIST -ne 0 || ( $VERSION_EXIST == 0 && $SECOND_VERSION -lt 8 ) ]]; then
            PYTHON_VERSION='python3.8'
            SECOND_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[1])'`
            VERSION_EXIST=$?
            if [[ $VERSION_EXIST -ne 0 || ( $VERSION_EXIST == 0 && $SECOND_VERSION -lt 8 ) ]]; then
                PYTHON_VERSION='python'
            fi
        fi
    fi
else
    PYTHON_VERSION='python3'
    SECOND_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[1])'`
    VERSION_EXIST=$?
    if [[ $VERSION_EXIST -ne 0 || ( $VERSION_EXIST == 0 && $SECOND_VERSION -lt 8 ) ]]; then
        PYTHON_VERSION='python3.8'
        SECOND_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[1])'`
        VERSION_EXIST=$?
        if [[ $VERSION_EXIST -ne 0 || ( $VERSION_EXIST == 0 && $SECOND_VERSION -lt 8 ) ]]; then
            PYTHON_VERSION='python3'
        fi
    fi
fi

FIRST_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[0])'`
VERSION_EXIST=$?
if [[ $VERSION_EXIST -ne 0 ]]; then
    PYTHON_VERSION='python'
    FIRST_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[0])'`
    VERSION_EXIST=$?
    if [[ $VERSION_EXIST -ne 0 ]]; then
        printf "Not Found Python In This Machine\n"
        exit 1
    fi
fi
FIRST_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[0])'`
SECOND_VERSION=`${PYTHON_VERSION} -c 'import sys; print(sys.version_info[1])'`
if [[ $FIRST_VERSION == 2 || ( $FIRST_VERSION -ge 3 && $SECOND_VERSION -lt 6 ) ]]; then
    printf "Python Version ${FIRST_VERSION}.${SECOND_VERSION} Is Not Used For This System\n"
    printf "Require Python 3.8 Or Above\n"
    exit 1
fi
echo $PYTHON_VERSION
exit 0
