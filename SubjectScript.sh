#!/bin/bash

cd SubjectCommitTest

rm -rf .git/

git init

git remote add origin $1

git pull
