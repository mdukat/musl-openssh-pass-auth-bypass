poc made by clanker, tested by me, a human

license: do whatever the f you want

tested against clean Alpine 3.24.0 Extended VM with user "ciota" which has set their password hash as "*" in /etc/shadow (manual change as root), and an additional user "canlogin" which has their password set and user is able to login to it via ssh.

alpine iso:
a9d8cc8c8176aabacde80d705569da102a90475f78424f57c8844612f2515511  alpine-extended-3.24.0-x86_64.iso

downloaded from: https://dl-cdn.alpinelinux.org/alpine/v3.24/releases/x86_64/alpine-extended-3.24.0-x86_64.iso

installed on a vm without internet access, repos skipped at install time, so openssh version stays vulnerable (OpenSSH_10.3p1).

note: user "ciota" was created with "adduser -S ciota", without setting it's password or anything else. this make it have /sbin/nologin set as their shell in /etc/passwd. script "openssh-exploit.py" can read files without shell access, so it generates "id" output by parsing /proc/self/status. please read and think for yourself, as clanker will try to make you believe some bullshit. after setting user's "ciota" shell to /bin/sh in /etc/passwd, script "openssh-generic-poc.py" works as intended - it can login as this user and execute commands on their behalf







lol





links:
 - https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/
 - www.openssh.com/releasenotes.html
 - https://sshhole.com/

