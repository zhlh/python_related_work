#!/usr/bin/env python
"""
This script is use for auto restricting expired SS account.
Script read and modify SS configure file shadowsocks.json file.
Restrict action is acctually change the password, which makes the user unable to login the SS server.
Account expired information stores in a account info text file.
account info file format:
port	start_dt	end_dt
80	2016-08-01	2016-09-01

And define 5 days buffer after end_dt comes, which means 
if the end_dt is 2016-09-01, acctully restricted date will be 2016-09-06.

All restricted info will be written in restrict.log file.
"""
import re
import json
import os
import sys
from datetime import datetime, timedelta
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_str_match_pattern(r_pattern, str_v):
    pat = re.compile(r_pattern)
    m = re.match(pat, str_v)
    if m: return True
    return False

def str2date(dt_str='', dt_format='%Y-%m-%d'):
    try:
       return datetime.strptime(dt_str, dt_format)
    except ValueError:
       logger.error('Invalid date string: {}'.format(dt_str))


def do_logger(msg=None, log_fn='/root/shadowsocks/restrict.log'):
    with open(log_fn, 'a') as f:
       f.write('{}\t{}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))
 

class AccountMgr:

    def __init__(self, ss_conf_fn='shadowsocks.json', acct_info_fn='account_info.txt'):
       self.ss_conf_fn = ss_conf_fn
       self.acct_info_fn = acct_info_fn
       self.buffer_days = 5
       self.conf_obj = None
       self.ports = None
       self.acct_info = None
       self.need_restrict_ports = None
       self._load_data()

    def _load_data(self):
       if not os.path.exists(self.ss_conf_fn):
          logger.error('SS server config file {} does not exist.'.format(self.ss_conf_fn))         
          sys.exit(1)
       if not os.path.exists(self.acct_info_fn):
          logger.error('SS account information file {} does not exist.'.format(self.acct_info_fn))
          sys.exit(2)

       self._load_ss_conf()
       self._load_acct_info()
       if self.conf_obj is None or self.acct_info is None:
          logger.error('Load data from file failed.')
          sys.exit(3)
       
    
    # load data for conf_obj and ports
    def _load_ss_conf(self):
       logger.info('Load data from SS config file {}...'.format(self.ss_conf_fn))
       with open(self.ss_conf_fn, 'r') as f:
          json_data = f.read()
          try:
             self.conf_obj = json.loads(json_data)
             if u'port_password' not in self.conf_obj.keys():
                logger.error('Not recongized SS config file format, no port_password key defined.')
                return
             port_password = self.conf_obj.get(u'port_password')
             if isinstance(port_password, dict):
                self.ports = [ int(x) for x in port_password.keys() ]
          except ValueError:
             logger.error('Invalid SS config file format, is not a valid json format file.')
             return

    # load account info
    def _load_acct_info(self):
       logger.info('Load data from acct info file {}...'.format(self.acct_info_fn))
       self.acct_info = {}
       with open(self.acct_info_fn, 'r') as f:
           for line in f.readlines():
               if is_str_match_pattern(r'^\s*(#|;).*$', line):
                  continue
               raw_data = re.sub(r'\s+', '\t', line.strip())
               raw_data = re.sub(r'\t+', '\t', raw_data)              
               acct_rec = raw_data.split('\t')
               if len(acct_rec) != 3:
                  logger.warn('Invalid account info data: "{}", missing or more fields, skip.'.format(line.strip()))
           
               port = None
               if is_str_match_pattern(r'^\d+$', acct_rec[0]):
                  port = int(acct_rec[0])
               else:
                  logger.error('Wrong port value: {}, should be a number'.format(acct_rec[0]))
                  continue

               if is_str_match_pattern(r'^\d{4}-\d{2}-\d{2}$', acct_rec[1]):
                  start_dt = str2date(dt_str=acct_rec[1])
               else:
                  logger.warn('Invalid start_dt value: {}'.format(acct_rec[1]))
                  start_dt = datetime.now()

               if is_str_match_pattern(r'^\d{4}-\d{2}-\d{2}$', acct_rec[2]):
                  end_dt = str2date(dt_str=acct_rec[2])
                  is_acct_limit = True
               elif is_str_match_pattern(r'^-$', acct_rec[2]):
                  is_acct_limit = False
                  end_dt = None
               else:
                  logger.warn('Unrecongized end_dt value: {} for port {}'.format(acct_rec[2], acct_rec[0]))   

               self.acct_info[unicode(port)] = { 'start_dt': start_dt, 'end_dt': end_dt, 'is_acct_limit': is_acct_limit, }           


    # check and get all expired account
    def _check_expired_acct(self):
       now = datetime.now()
       self.need_restrict_ports = []
       for port, acct_info in self.acct_info.items():
           is_acct_limit = acct_info.get('is_acct_limit')
           if not is_acct_limit:
              logger.info('Port {} is unlimited.'.format(port))
              continue
           end_dt = acct_info.get('end_dt')
           
           if now <= end_dt + timedelta(days=self.buffer_days):
              logger.info('Port {} is in service.'.format(port))
           else:
              logger.warn('Port {} is expired and will be restircted'.format(port))
              self.need_restrict_ports.append(port)


    # restrict expired account, change the password to the specified port, if the password is end with '_expired' do nothing, or append '_expired'
    def _restrict_expired_accts(self):
       obj_changes = 0
       if len(self.need_restrict_ports) == 0:
          logger.info('No expired account found, check time: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
          return
       for port in self.need_restrict_ports:
          old_pass = self.conf_obj.get('port_password').get(port)
          if not old_pass.endswith('_expired'): 
             obj_changes = 1
             self.conf_obj['port_password'][port] = '{}_expired'.format(old_pass)
             end_dt = self.acct_info.get(port).get('end_dt')
             end_dt_str = end_dt.strftime('%Y-%m-%d')
             logger.info('Port {} is expired, expire date is {}, do restriction on port {}.'.format(port,end_dt_str,port))
             do_logger('Port {} is expired, expire date is {}, do restriction on port {}.'.format(port,end_dt_str,port))
          else:
             logger.warn('Port {} has already been restricted'.format(port))
             # do_logger('Port {} has already been restricted'.format(port))
       logger.debug('CONF_OBJ: {}'.format(self.conf_obj))
       # write new acct into to SS config file
       if obj_changes == 1:
          with open(self.ss_conf_fn, 'w') as f:
             f.write(json.dumps(self.conf_obj,sort_keys=True,indent=4))
          logger.info('Finish restricting expired acct and override SS config file {}.'.format(self.ss_conf_fn))
       else:
          logger.info('No changes to SS config file {}.'.format(self.ss_conf_fn))


    # Control fun
    def process(self):
       self._check_expired_acct()
       self._restrict_expired_accts()


def main():
   ss_conf_fn = '/etc/shadowsocks.json'
   acct_info_fn = '/root/shadowsocks/account_info.txt'
   
   am = AccountMgr(ss_conf_fn=ss_conf_fn, acct_info_fn=acct_info_fn)
   am.process()


if __name__=='__main__':
   main()
