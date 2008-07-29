#!/bin/bash

rm testing.sqlite
touch testing.sqlite
if (( $? )) ; then
  echo "Unable to create database. Check Django does not running and try again."
  exit 1
fi

./manage.py syncdb
if (( $? )) ; then
  echo "Unable to create new schema (syncdb)."
  exit 1
fi
