# Linux Exercises

## PART 1 — File Management

**Task 1 — Create Project Structure**

```bash
mkdir -p ~/devops-project/{logs,backups,scripts,configs,temp}
```

Verified with:

```bash
find ~/devops-project -type d
```

Output:
```
/home/k-22/devops-project
/home/k-22/devops-project/scripts
/home/k-22/devops-project/configs
/home/k-22/devops-project/backups
/home/k-22/devops-project/logs
/home/k-22/devops-project/temp
```

**Task 2 — Create Files**

```bash
touch ~/devops-project/logs/app.log
touch ~/devops-project/scripts/deploy.sh
touch ~/devops-project/configs/app.conf
```

Verified:
```
/home/k-22/devops-project/scripts/deploy.sh
/home/k-22/devops-project/configs/app.conf
/home/k-22/devops-project/logs/app.log
```

**Task 3 — Add Sample Content**

```bash
cat > ~/devops-project/logs/app.log <<EOF
INFO Server started
WARNING Disk almost full
ERROR Database connection failed
INFO User login successful
EOF
```

**Task 4 — Copy Backup**

```bash
cp ~/devops-project/configs/app.conf ~/devops-project/backups/
```

Both locations now have the file:
```
/home/k-22/devops-project/configs/app.conf
/home/k-22/devops-project/backups/app.conf
```

## PART 2 — File Viewing & Log Investigation

**Task 5 — Investigate Logs**

```bash
grep "ERROR" ~/devops-project/logs/app.log
grep "WARNING" ~/devops-project/logs/app.log
```

Output:
```
ERROR Database connection failed
WARNING Disk almost full
```

**Task 6 — Monitor Logs Live**

```bash
tail -f ~/devops-project/logs/app.log
```

The `-f` flag keeps watching the file and prints new lines as they are written.

## PART 3 — Permissions & Ownership

**Task 7 — Script Permissions**

```bash
chmod +x ~/devops-project/scripts/deploy.sh
ls -la ~/devops-project/scripts/deploy.sh
```

Output:
```
-rwxrwxr-x 1 k-22 k-22 0 May 19 00:45 /home/k-22/devops-project/scripts/deploy.sh
```

**Task 8 — Secure Config File**

```bash
chmod 600 ~/devops-project/configs/app.conf
ls -la ~/devops-project/configs/app.conf
```

Output:
```
-rw------- 1 k-22 k-22 0 May 19 00:45 /home/k-22/devops-project/configs/app.conf
```

**Task 9 — Explain Permissions**

755 means the owner can read, write and execute. Group and others can read and execute but not write. Standard for scripts.

644 means the owner can read and write. Group and others can only read. Standard for config files and documents.

600 means only the owner can read and write. Nobody else has any access at all. Used for sensitive files.

## PART 4 — Process Management

**Task 10 — Start Background Process**

```bash
sleep 500 &
```

Output:
```
[1] 95272
```

**Task 11 — Identify Process**

```bash
jobs
```

Output:
```
[1]+  Running    sleep 500 &
```

```bash
ps aux | grep sleep
```

Output:
```
k-22   95272  0.0  0.0  16112  7796 pts/1    S    00:45   0:00 sleep 500
k-22   95292  0.0  0.0  18000  2668 pts/1    S+   00:45   0:00 grep --color=auto sleep
```

PID is 95272, process name is sleep.

**Task 12 — Terminate Process**

```bash
kill 95272
```

This sends SIGTERM. If the process does not stop, use `kill -9 95272` to force kill it.

**Task 13 — Monitor System**

```bash
ps aux
free -h
```

Output from `free -h`:
```
               total        used        free      shared  buff/cache   available
Mem:            14Gi       9.6Gi       1.7Gi       1.9Gi       5.9Gi       5.3Gi
Swap:          4.0Gi        11Mi       4.0Gi
```

## PART 5 — Networking & Connectivity

**Task 14 — Find Server IP**

```bash
ip a
```

Relevant output:
```
3: wlp58s0:
    inet 10.111.243.37/16 brd 10.111.255.255 scope global dynamic noprefixroute wlp58s0
```

IP is 10.111.243.37 on Wi-Fi interface wlp58s0.

**Task 15 — Test Connectivity**

```bash
ping -c 4 google.com
```

Output:
```
PING google.com (216.58.223.78) 56(84) bytes of data.
64 bytes from mba01s07-in-f14.1e100.net (216.58.223.78): icmp_seq=1 ttl=1 time=11.1 ms
64 bytes from mba01s07-in-f14.1e100.net (216.58.223.78): icmp_seq=2 ttl=1 time=23.8 ms
64 bytes from mba01s07-in-f14.1e100.net (216.58.223.78): icmp_seq=3 ttl=1 time=11.7 ms
64 bytes from mba01s07-in-f14.1e100.net (216.58.223.78): icmp_seq=4 ttl=1 time=11.8 ms

4 packets transmitted, 4 received, 0% packet loss, time 3004ms
```

**Task 16 — Verify Listening Ports**

```bash
ss -tulnp
ss -tulnp | grep :22
ss -tulnp | grep :80
```

## PART 6 — SSH & SCP

**Tasks 17, 18, 19**

I could not complete these tasks. AWS kept rejecting my ID during account verification so I was not able to create an EC2 instance. I will complete this section once the account issue is resolved.

## PART 7 — Disk & System Information

**Task 20 — Check System Resources**

```bash
free -h
df -h
uptime
uname -a
```

Output:
```
Mem:   14Gi total   9.6Gi used   1.7Gi free   5.3Gi available
Swap:  4.0Gi total    11Mi used   4.0Gi free

/dev/nvme0n1p2  468G   26G  418G   6% /

00:45:45 up 1 day, 8:20, 1 user, load average: 1.04, 1.09, 1.12

Linux k-22 7.0.0-15-generic #15-Ubuntu SMP PREEMPT_DYNAMIC Wed Apr 22 16:06:43 UTC 2026 x86_64 GNU/Linux
```

**Task 21 — Analyze Storage**

```bash
du -sh ~/devops-project
df -h /
```

Output:
```
28K    /home/k-22/devops-project

/dev/nvme0n1p2  468G   26G  418G   6% /
```

## PART 8 — Compression & Backups

**Task 22 — Create Backup Archive**

```bash
cd ~
tar -czvf devops-backup.tar.gz devops-project/
```

Output:
```
devops-project/
devops-project/scripts/deploy.sh
devops-project/configs/app.conf
devops-project/backups/app.conf
devops-project/logs/app.log
devops-project/temp/
```

**Task 23 — Extract Backup**

```bash
mkdir -p ~/restore
tar -xzvf devops-backup.tar.gz -C ~/restore/
ls ~/restore/
```

Output:
```
devops-project
```
