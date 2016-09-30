#!/bin/bash

MONITOR_SCRIPT='/root/list_active_ports.sh'
LOG_FILE="/root/shadowsocks/monitor_ss_port_use_$(date +'%Y%m%d').log"
TMP_FILE="/tmp/tmp.port_use"

main(){
   bash ${MONITOR_SCRIPT}  > ${TMP_FILE} 2>&1
   lines=`cat ${TMP_FILE} | wc -l`
   if [ ${lines} -gt 0 ]; then
      echo "--$(date +'%F %T') start +++++++++++++++++++++++++++++++++++++++++++++" >> ${LOG_FILE}
      cat ${TMP_FILE} >> ${LOG_FILE}
      echo "--$(date +'%F %T') end   +++++++++++++++++++++++++++++++++++++++++++++" >> ${LOG_FILE}
   fi
   # echo "Log file path : ${LOG_FILE}."
}


main
