#!/bin/bash
SMASHDIR="/root/smashdir"
LASTDATE=$(date +%Y-%m-%d -d "-4 days")

for entry in "$SMASHDIR"/*
do
  FILEDATE=$(stat -c %y $entry | cut -d'.' -f1 | cut -d' ' -f1)

  if [[ $FILEDATE < $LASTDATE ]]
  then
    echo $entry
    rm -rf $entry
  fi
done

