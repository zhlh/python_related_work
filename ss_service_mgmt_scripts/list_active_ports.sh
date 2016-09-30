#!/bin/bash

eth0_ip=$(ifconfig eth0 | grep "inet addr" | cut -d: -f 2 | cut -d" " -f 1)
echo "Current eth0 IP: ${eth0_ip}"
netstat -anlut | grep -v '0.0.0.0:*' | grep -E "${eth0_ip}:\<(8089|80|50000|21|22|6666|3389|18384|18383|18382|18381|443|60000|8008|7001|28007|28006|28005|28004|28003|28002|28001)\>" | awk '{print $4}' | sort | awk -F: '{print $2}' | uniq -c
