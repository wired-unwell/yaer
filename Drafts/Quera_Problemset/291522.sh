#!/usr/bin/env bash

# Siahe-ye Agha Mamad

file=$(<quera.md)
#file="![a](1.png) some text ![b](2.png) ![c](3.png)"

parags=()

imgpattern='(.*?)!\[[^]]*]\([^\)]+\)(.*)'
pattern=$imgpattern
while [[ $file =~ $pattern ]]; do
	parags+=("${BASH_REMATCH[1]}")
	file="${BASH_REMATCH[2]}"
done;

parags+=("$file")

maxlength=0

for par in "${parags[@]}";
	do
	if [[ ${#par} -gt $maxlength ]]; then
		maxlength=${#par}
	fi
done

if [[ $maxlength -gt 200 ]]; then
	echo "YES"
	#exit 0
else
	echo "NO"
fi

#echo "NO"
#exit 0
