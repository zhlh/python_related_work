# Script function

This script is use for auto restricting SS port if there have port's end_dt old than the current date.

Port and end_dt info is defined in **account_info.txt** file.

In fact, the restricted action is simple, just change the expired ports' password and then restart SS service.

Each run will have logs insert into file **~root/shadowsocks/restrict.log**.

# Script usage

```bash
/root/python_related_work/ss_acct_restrict/ss_expired_acct_check.py
```

# Deploy with crontab

```
# Do auto restriction every day at 1:00
0 1 * * * /root/python_related_work/ss_acct_restrict/ss_expired_acct_check.py
```

