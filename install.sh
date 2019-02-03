#!/bin/bash

prog=( boxes figlet cmatrix lolcat python-wit toilet trash-cli )

for p in ${prog[@]}
do
	printf "Installing: $p\n"
	apt -y install $p
done

