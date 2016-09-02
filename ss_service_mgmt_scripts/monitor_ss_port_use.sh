#!/bin/bash

MONITOR_SCRIPT='/root/list_active_ports.sh'
LOG_FILE='/root/shadowsocks/monitor_ss_port_use.log'

main(){
   echo "--$(date +'%F %T') start +++++++++++++++++++++++++++++++++++++++++++++" >> ${LOG_FILE}
   bash ${MONITOR_SCRIPT}  >> ${LOG_FILE} 2>&1
   echo "--$(date +'%F %T') end   +++++++++++++++++++++++++++++++++++++++++++++" >> ${LOG_FILE}
   # echo "Log file path : ${LOG_FILE}."
}


main
