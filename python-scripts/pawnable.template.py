from pwn import *

# ------------------- CONFIG -------------------
CHALLENGE_NAME = ''  # change to match the challenge folder
PASSWORD = 'guest'      # change if needed
PORT = 2222
HOST = 'pwnable.kr'
BINARY_PATH = f'./{CHALLENGE_NAME}'  # binary to execute

USE_SSH = True    # False if local only
USE_GDB = False   # Set to True to enable GDB

ENV = {"PATH": "/bin:/usr/bin"}  # in case PATH is needed
# ---------------------------------------------


def start_process(ssh_session=None):
    if ssh_session:
        return ssh_session.process(BINARY_PATH, env=ENV)
    else:
        return process(BINARY_PATH)


def attach_debugger(proc):
    if USE_GDB:
        gdb.attach(proc, '''
            b main
            c
        ''')


def main():
    if USE_SSH:
        log.info("Connecting via SSH...")
        s = ssh(host=HOST, user=CHALLENGE_NAME, password=PASSWORD, port=PORT)
        p = start_process(s)
    else:
        log.info("Running binary locally...")
        p = start_process()

    attach_debugger(p)

    # ---------------- EXPLOIT GOES HERE ----------------
    payload = b''
    p.sendline(payload)

    # Print banner or first output lines safely
    try:
        output = p.recvline(timeout=1)
        if output:
            print(output.decode(errors='ignore'))
    except EOFError:
        pass

    # Start interactive session
    p.interactive()
    # ---------------------------------------------------


if __name__ == "__main__":
    main()
