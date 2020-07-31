#on sciget
# everyday, delete files older than 728 days in adwilk dir
0 3 * * * find /project/wang4/users/adwilk/ -type f -mtime +728 -delete


#on database server
# at 12:01am, first of every month, run archive script
1 0 1 * * bash $PWD/run-backup.sh
