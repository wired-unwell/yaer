#!/usr/bin/env bash

groupadd quera-bootcamp
useradd -G quera-bootcamp user1 --password user1pass -m -d /home/user1
useradd -G quera-bootcamp user2 --password user2pass -m -d /home/user2
mkdir /bootcamp
touch /bootcamp/bootcamp_data
chown -r user1:quera-bootcamp /bootcamp/bootcamp_data
chmod 660 /bootcamp/bootcamp_data
userdel -r user1
userdel -r user2
groupdel quera-bootcamp
rm -f /bootcamp/bootcamp_data
rm -fr /bootcamp
