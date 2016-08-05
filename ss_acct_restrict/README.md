# Script function

This script is use for restrict SS port if the port end_dt is old than the current date.

Port and end_dt info is defined in **account_info.txt** file.

In fact, the restricted action is simple, just change the expired ports' password and then restart SS service.

Each run will have logs insert into file **~root/shadowsocks/restrict.log**.

# Script usage

```bash
./python_related_work/ss_acct_restrict/ss_expired_acct_check.py
```
