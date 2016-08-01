#!/bin/env python
# coding: utf-8
"""
  Assume your logfile is one of the following format:
     1. ^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ (\w+) .*$
     2. ^Log4j:\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+(\w+) .*$

  This script can parser the above two format logfiles, and provide you a way to 
  list the log records between the start_timestamp and end_timestamp with specified 
  log record type.
  Normally log record type can be DEBUG, INFO, WARN, ERROR.
"""

import re
import os
import sys
from datetime import datetime

DT_FORMAT = '%Y-%m-%d %H:%M:%S'

# Covert date string to date
def to_date(_dt_value=None, _dt_format=DT_FORMAT):
   if _dt_value is None:
      return None
   return datetime.strptime(_dt_value, _dt_format)

# Check if the given date is between dt_start and dt_end
def is_dt_ok(dt, dt_start, dt_end):
    if dt_start <= dt and dt_end >= dt:
       return True
    else:
       return False

# Filter all qualified records
def filter_records(logfile, dt_start, dt_end, keyword):
   if not os.path.exists(logfile):
      print('Log File {} does not exist.'.format(logfile))
      return None
   if isinstance(dt_start, str): dt_start = to_date(_dt_value=dt_start)
   if isinstance(dt_end, str): dt_end = to_date(_dt_value=dt_end)
   qualified_records = []
   append_following_lines = False
   log_begin_flag = False
   with open(logfile, 'r') as f:
      single_log_record_lines = []
      for line in f:
         line = line.strip()
         # support log format: LOG_TIMESTAMP LOG_TYPE LOG_MESSAGE
         m = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ (\w+) .*$', line)
         if m is None:
            # support log format: Log4j:[LOG_TIMESTAMP] LOG_TYPE LOG_MESSAGE
            m = re.match(r'^Log4j:\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+(\w+) .*$', line)
         if m:
            log_dt_str, log_type = m.groups()
            log_dt = to_date(_dt_value=log_dt_str, _dt_format=DT_FORMAT)
            if log_type.upper() != keyword.upper() or not is_dt_ok(log_dt, dt_start, dt_end):
               log_begin_flag = False
               append_following_lines = False 
               if single_log_record_lines:
                  qualified_records.append('\n'.join(single_log_record_lines))
                  single_log_record_lines = []
               continue
            single_log_record_lines.append(line)
            #print('Append Line: {}'.format(line))
            log_begin_flag = True
            append_following_lines = True
         else:
            if append_following_lines and log_begin_flag:
               single_log_record_lines.append(line)
               #print('Append Line: {}'.format(line))
               
      if single_log_record_lines:
         qualified_records.append('\n'.join(single_log_record_lines))     

   return qualified_records

def usage():
    print('''
Usage: python {} start_dt end_dt log_type logfile_path
    start_dt and end_dt should given value as format yyyy-mm-dd HH24:MM:SS
    log_type should be info, error, warning ...
'''.format(os.path.abspath(__file__)))

def check_dt_format_match(dt_value=None, dt_format=DT_FORMAT):
    if dt_value is None:
       return False
    m = re.match(r'^{}$'.format(dt_format), dt_value)
    if m:
       return True
    else:
       return False



def main():
    if len(sys.argv) != 5:
       usage()
       return
    start_dt = sys.argv[1]
    end_dt = sys.argv[2]
    log_type = sys.argv[3]
    logfile = sys.argv[4]
    if not os.path.exists(logfile):
       print('Log file {} does not exists.'.format(logfile))
       return
    if not check_dt_format_match(dt_value=start_dt) and check_dt_format_match(dt_value=end_dt):
       print('invalid format date value provide.')
       usage()
       return
    
    qualified_records = filter_records(logfile, start_dt, end_dt, log_type)
    print('#'*100)
    print('Start Time: {}'.format(start_dt))
    print('  End Time: {}'.format(end_dt))
    print('   Keyword: {}'.format(log_type))
    print('Log File Path: {}'.format(os.path.abspath(logfile)))
    print('Matched Log records list below:')
    print('#'*100)
    print('\n'.join(qualified_records))

if __name__=='__main__':
   main()
