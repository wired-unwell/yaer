#!/usr/bin/env bash

message="Hello Code Star 1404, I'm Back!"

new_message=""

for ((i=0; i<${#message}; i++)); do
	new_message=$(echo $new_message"\x"$(printf "%02x " "'${message:i:1}"))
done

echo $new_message
