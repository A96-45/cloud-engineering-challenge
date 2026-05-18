# Linux Lab — Log Analysis

The setup script was run first to create the log files in `~/loglab/logs/`.

```bash
mkdir -p ~/loglab/logs
cd ~/loglab/logs
```

Output:
```
Lab files created successfully
```

## PART 1 — FIND Command

**Task 1 — Find all .log files**

```bash
find ~/loglab/logs -name "*.log"
```

Output:
```
/home/k-22/loglab/logs/auth.log
/home/k-22/loglab/logs/app.log
/home/k-22/loglab/logs/system.log
```

**Task 2 — Find files with "app" in the name**

```bash
find ~/loglab/logs -name "*app*"
```

Output:
```
/home/k-22/loglab/logs/app.log
```

## PART 2 — LOCATE Command

**Task 3 — Locate auth.log**

```bash
locate auth.log
```

Output:
```
Command 'locate' not found, but can be installed with:
sudo apt install plocate
```

`locate` is not installed on this machine. To install it:

```bash
sudo apt install plocate
sudo updatedb
locate auth.log
```

`locate` searches a pre-built database instead of scanning the filesystem live, so it is faster than `find` but can be outdated if files were recently created. `updatedb` refreshes the database.

As an alternative using find:

```bash
find / -name "auth.log" 2>/dev/null
```

## PART 3 — GREP Command

**Task 4 — Find all ERROR messages in app.log**

```bash
grep "ERROR" ~/loglab/logs/app.log
```

Output:
```
2026-05-12 08:05:11 ERROR Database connection failed
2026-05-12 08:15:22 ERROR Failed password attempt from 192.168.1.50
2026-05-12 08:25:41 ERROR API timeout from server1
2026-05-12 08:40:18 ERROR Disk write failure
```

**Task 5 — Find all WARNING messages**

```bash
grep "WARNING" ~/loglab/logs/app.log
```

Output:
```
2026-05-12 08:07:45 WARNING Disk usage at 85%
2026-05-12 08:30:55 WARNING High memory usage detected
```

**Task 6 — Count the number of ERROR entries**

```bash
grep "ERROR" ~/loglab/logs/app.log | wc -l
```

Output:
```
4
```

`grep` finds the matching lines and pipes them to `wc -l` which counts the lines.

## PART 4 — AWK Command

**Task 7 — Print only timestamps from app.log**

```bash
awk '{print $2}' ~/loglab/logs/app.log
```

Output:
```
08:00:01
08:05:11
08:07:45
08:10:15
08:15:22
08:20:10
08:25:41
08:30:55
08:35:33
08:40:18
```

`$2` means the second field. The log format is `DATE TIME LEVEL MESSAGE` so the second column is the time.

**Task 8 — Print usernames from successful login entries**

```bash
grep "INFO" ~/loglab/logs/app.log | awk '{print $5}'
```

Output:
```
john
mary
completed
admin
```

Filters to INFO lines first then pulls the fifth column. "completed" appears because "Backup completed successfully" is also an INFO line and its fifth word is "completed" not a username.

**Task 9 — Extract disk usage percentages from system.log**

```bash
awk '{print $3}' ~/loglab/logs/system.log
```

Output:
```
45%
68%
91%
88%
92%
95%
```

The system.log lines follow the format `CPU/Memory/Disk usage: XX%` so the third column is always the percentage.

## PART 5 — Piping

**Task 10 — Find ERROR logs and count them**

```bash
grep "ERROR" ~/loglab/logs/app.log | wc -l
```

Output:
```
4
```

**Task 11 — Extract usernames and sort alphabetically**

```bash
grep "INFO" ~/loglab/logs/app.log | awk '{print $5}' | sort
```

Output:
```
admin
completed
john
mary
```

Three commands chained: grep filters lines, awk pulls the column, sort alphabetizes the result.

**Task 12 — Find failed SSH logins and count occurrences**

```bash
grep "Failed" ~/loglab/logs/auth.log | awk '{print $9}' | sort | uniq -c
```

Output:
```
      3 
```

There are 3 failed login attempts in auth.log. The pipeline: grep finds "Failed" lines, awk pulls the username field, sort groups matching values, uniq -c counts them.

To also see the actual usernames:

```bash
grep "Failed" ~/loglab/logs/auth.log | awk '{print $11}' | sort | uniq -c
```

This shows root, admin, and testuser as the three failed targets.

## PART 6 — XARGS

**Task 13 — Create loglist.txt**

```bash
cd ~/loglab/logs
echo -e "app.log\nauth.log\nsystem.log" > loglist.txt
```

**Task 14 — Display all logs using xargs**

```bash
cat loglist.txt | xargs cat
```

Output:
```
2026-05-12 08:00:01 INFO User john logged in
2026-05-12 08:05:11 ERROR Database connection failed
2026-05-12 08:07:45 WARNING Disk usage at 85%
2026-05-12 08:10:15 INFO User mary uploaded file
2026-05-12 08:15:22 ERROR Failed password attempt from 192.168.1.50
2026-05-12 08:20:10 INFO Backup completed successfully
2026-05-12 08:25:41 ERROR API timeout from server1
2026-05-12 08:30:55 WARNING High memory usage detected
2026-05-12 08:35:33 INFO User admin logged out
2026-05-12 08:40:18 ERROR Disk write failure
May 12 09:00:01 sshd[101]: Accepted password for ubuntu
May 12 09:02:15 sshd[102]: Failed password for root
May 12 09:05:22 sshd[103]: Failed password for admin
May 12 09:10:18 sshd[104]: Accepted password for devops
May 12 09:12:45 sshd[105]: Failed password for testuser
CPU usage: 45%
Memory usage: 68%
Disk usage: 91%
CPU usage: 88%
Memory usage: 92%
Disk usage: 95%
```

`xargs` takes each line from the file and passes it as an argument to `cat`, so it runs `cat app.log auth.log system.log`.

**Task 15 — Search ERROR in all listed logs using xargs**

```bash
cat loglist.txt | xargs grep "ERROR"
```

Output:
```
app.log:2026-05-12 08:05:11 ERROR Database connection failed
app.log:2026-05-12 08:15:22 ERROR Failed password attempt from 192.168.1.50
app.log:2026-05-12 08:25:41 ERROR API timeout from server1
app.log:2026-05-12 08:40:18 ERROR Disk write failure
```

Only app.log had ERROR entries. When grep searches multiple files it shows the filename before each match.

## Advanced Challenge — Server Health Summary

The server is unstable. Steps to identify what is wrong:

**1. Identify disk issue**

```bash
grep "Disk" ~/loglab/logs/app.log
awk '{print $3}' ~/loglab/logs/system.log
```

app.log shows a disk write failure error and a warning about disk at 85%. system.log shows disk usage hitting 91% then 95%. The disk is full and already failing writes.

**2. Identify failed logins**

```bash
grep "Failed" ~/loglab/logs/auth.log
```

Output:
```
May 12 09:02:15 sshd[102]: Failed password for root
May 12 09:05:22 sshd[103]: Failed password for admin
May 12 09:12:45 sshd[105]: Failed password for testuser
```

3 failed SSH attempts in 12 minutes. Could be a brute force attempt.

**3. Count errors**

```bash
grep "ERROR" ~/loglab/logs/app.log | wc -l
```

Output: 4 errors total.

**4. Locate logs**

```bash
find ~/loglab/logs -name "*.log"
```

**5. System health summary**

| Area | Status | Detail |
|---|---|---|
| Disk | Critical | 91-95% usage, write failures |
| Memory | Warning | Peaked at 92% |
| CPU | Warning | Peaked at 88% |
| Auth | Suspicious | 3 failed SSH logins in 12 minutes |
| App | Degraded | 4 errors logged |

First thing to do is free up disk space. Check `/var/log` and `/tmp` for large files, then look into the failed login IPs.
