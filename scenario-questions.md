# Scenario Questions

## File Management Scenarios

**1. You accidentally created a file in the wrong directory. How would you move it to `/home/ubuntu/projects`?**

```bash
mv wrongfile.txt /home/ubuntu/projects/
```

If you are not sure where you created it, find it first with `find ~ -name "wrongfile.txt"` then move it.

**2. Your team needs a folder structure for logs, scripts, and backups. How would you create all folders using one command?**

```bash
mkdir -p /home/ubuntu/{logs,scripts,backups}
```

The `-p` flag creates parent directories if they do not exist. The brace expansion creates all three folders in one go.

**3. A backup file is consuming space. How would you locate it, copy it to a backup directory, then delete the original?**

```bash
find / -name "backup-file.tar.gz" 2>/dev/null
cp /path/to/backup-file.tar.gz /home/ubuntu/backups/
rm /path/to/backup-file.tar.gz
```

Always copy first and confirm the copy exists before deleting the original.

## File Viewing & Management Scenarios

**4. A web application is failing. The logs are in `/var/log/app.log`. How would you view the latest logs and continuously monitor updates?**

```bash
tail -50 /var/log/app.log
tail -f /var/log/app.log
```

`tail -f` keeps the file open and prints new lines as they arrive. You open a second terminal, trigger the failing action, and watch what gets logged.

**5. You suspect the application has database errors. How would you search the log file for ERROR?**

```bash
grep "ERROR" /var/log/app.log
grep "ERROR" /var/log/app.log | wc -l
```

The second command counts how many errors exist, which is useful if the log is large.

**6. A configuration file is very large. Which command would help you scroll through it page by page?**

```bash
less /etc/someconfig.conf
```

`less` lets you scroll up and down without loading the whole file at once. Use Space to go forward, `b` to go back, `/searchterm` to search inside it, and `q` to quit.

## Permissions & Ownership Scenarios

**7. A deployment script called deploy.sh fails with "Permission denied". How would you fix it?**

```bash
chmod +x deploy.sh
```

The file does not have the execute bit set so Linux will not run it. `chmod +x` adds execute permission.

**8. You want only the owner to read, write, and execute a file. Which permission number would you use?**

```bash
chmod 700 filename
```

7 gives the owner read, write and execute. The two zeros give group and others nothing at all.

**9. A file belongs to the wrong user. How would you change ownership to ubuntu?**

```bash
sudo chown ubuntu filename
```

You need `sudo` because changing ownership is a privileged operation.

**10. You accidentally gave everyone write access to a sensitive file. Why is this dangerous?**

Any user on the system can modify or overwrite the file. For a config file that means someone could change passwords or API keys without needing admin access. For a script it means someone could inject commands that run the next time the script is executed, possibly as root if it is in a cron job.

## Process Management Scenarios

**11. A Python application is consuming 95% CPU. Which commands would help you identify the process?**

```bash
top
ps aux --sort=-%cpu | head -10
ps aux | grep python
```

`top` shows a live list sorted by CPU usage. The problematic process will sit at the top. Note the PID from the output.

**12. A background process named sleep is still running. How would you stop it?**

```bash
ps aux | grep sleep
kill <PID>
```

If it does not stop: `kill -9 <PID>` or `pkill sleep`. Always try the normal kill first before forcing it.

**13. Your server becomes slow. Why is checking running processes important?**

Something is using more resources than it should. Checking with `top` or `ps aux` shows exactly which process is eating CPU or RAM so you can deal with it directly instead of guessing.

**14. You started a process accidentally in the background. How would you view background jobs?**

```bash
jobs
```

Lists all background jobs in the current shell session. Use `fg %1` to bring one to the foreground or `kill %1` to stop it.

## Networking & Connectivity Scenarios

**15. A student cannot connect to the internet from the Linux VM. Which command would you use first to test connectivity?**

```bash
ping -c 4 google.com
```

If that fails, try pinging an IP directly with `ping -c 4 8.8.8.8`. If the IP works but the domain does not, the problem is DNS. If neither works, it is a network or routing issue.

**16. You need to know the IP address of your Linux server. Which command would you use?**

```bash
ip a
```

Look for the `inet` line under the active interface. On my machine it showed `inet 10.111.243.37/16` under `wlp58s0`.

**17. A web server should be listening on port 80. Which command helps confirm this?**

```bash
ss -tulnp | grep :80
```

If nothing shows up the web server is not running or is bound to a different port.

**18. A website domain is not resolving correctly. Which commands can help troubleshoot DNS?**

```bash
nslookup example.com
dig example.com
dig @8.8.8.8 example.com
```

`nslookup` gives a quick answer. `dig` gives the full DNS response with more detail. The last one queries Google's DNS directly to check if the issue is your local resolver or the domain itself.

## SSH & Remote Access Scenarios

**19. You need to remotely manage a Linux server from Windows. Which command would you use?**

```bash
ssh ubuntu@<server-ip>
ssh -i C:\path\to\key.pem ubuntu@<server-ip>
```

SSH is available in Windows PowerShell from Windows 10 onwards so no extra software is needed.

**20. You need to securely transfer backup.tar.gz from your local machine to a remote Linux server. Which command would you use?**

```bash
scp backup.tar.gz ubuntu@<server-ip>:/home/ubuntu/
scp -i your-key.pem backup.tar.gz ubuntu@<server-ip>:/home/ubuntu/
```

SCP uses the SSH connection so everything is encrypted. For large files or syncing directories `rsync` is better because it only transfers what changed.

## Bonus Challenge Questions

**21. Why is Linux heavily used in cloud computing and DevOps?**

It is free and open source so there is no licensing cost per server, which matters a lot at cloud scale. It is also stable. Linux servers run for years without needing a reboot. Everything is configurable from the command line so automation is straightforward. Tools like Ansible, Docker and Terraform all work around this. You write the commands once and they run the same way on every machine. Most cloud providers also default to Linux for their VMs and the container ecosystem runs on Linux natively.

**22. What is the difference between chmod 755 and chmod 644?**

755 gives the owner full access and lets group and others read and execute but not write. Used for scripts and directories since you need execute to enter a directory or run a script.

644 gives the owner read and write access. Group and others can only read. Used for normal files like config files or documents that other users might need to read but should not edit.

The main difference is the execute bit. Regular files do not need it unless they are scripts.

**23. Why is `chmod +x script.sh` important before running scripts?**

Linux does not treat a file as executable just because it ends in `.sh`. Without the execute bit set you get "Permission denied" when you try to run it. `chmod +x` sets that bit. You can bypass it by running `bash script.sh` but that does not work for cron jobs or systemd services that call the script by path, so setting the bit properly is the right way.

**24. Why is SSH considered more secure than older remote access methods?**

Older tools like Telnet send everything as plain text including passwords. Anyone on the same network can read them with a packet sniffer. SSH encrypts the whole session so intercepted traffic is unreadable. It also supports key-based authentication where you never send a password over the wire at all. The server just checks that your private key matches the public key it has on file. SSH also verifies the server's identity through host key fingerprints which stops someone from pretending to be the server.

**25. Why is process management important in Docker and Kubernetes environments?**

In Docker each container runs one main process. If that process dies the container stops. How you start, signal and shut down processes directly affects whether containers behave reliably. A script that does not handle SIGTERM properly causes containers to hang during shutdown.

In Kubernetes it scales up. Kubernetes watches whether the main process in each pod is still running and restarts it if it crashes. Liveness and readiness probes also depend on processes responding correctly. Resource limits in Kubernetes are set per container and if a process exceeds its memory limit the container gets killed. Knowing how to use `ps`, `top` and `kill` is necessary for diagnosing why a pod is misbehaving.
