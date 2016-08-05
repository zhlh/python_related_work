#!/bin/bash

LOGFILE='/root/shadowsocks/auto_empty_iptables_rules.log'

empty_iptables_rule(){
   echo "==============================start $(date +'%F %T')==============================="  >> ${LOGFILE}
   # Save iptables rules to logfile
   /sbin/iptables -S >> ${LOGFILE}
   # Empty iptables INPUT rules
   /sbin/iptables -F
   echo "==================================================================================="  >> ${LOGFILE}
}


empty_iptables_rule
