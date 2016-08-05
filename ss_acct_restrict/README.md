# Script brief description

This script is use for restrict SS port if the port end_dt is old than the current date.

Port and end_dt info is defined in **account_info.txt** file.

In fact the restricted action is change the given port's password and restart SS service if there has expired ports.

Each run will have logs insert into file **~root/shadowsocks/restrict.log**.

## Script use

```bash
./python_related_work/ss_acct_restrict/ss_expired_acct_check.py
```
