#!/bin/bash -l

. scripts/setenv
if [[ $1 == 'clean' ]];then
	scons --clean -Q
else
	scons -Q with_features=$1
fi