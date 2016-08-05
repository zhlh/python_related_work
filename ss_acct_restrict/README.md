# Script brief description

This script is use for restrict SS port if the port end_dt is old than the current date.
Port and end_dt info is defined in acct_info.txt file.
In fact the restricted action is change the given port's password and restart SS service if there has expired ports.

Each runs will have logs insert into file ~root/shadowsocks/restrict.log.

## Script use

```bash
full_path_of_script
```
