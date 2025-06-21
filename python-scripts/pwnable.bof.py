from pwn import *

# ------------------- CONFIG -------------------
CHALLENGE_NAME = 'bof'  # change to match the challenge folder
PASSWORD = 'guest'  # change if needed
PORT = 2222
HOST = 'pwnable.kr'
BINARY_PATH = f'./{CHALLENGE_NAME}'  # binary to execute

USE_SSH = True  # False if local only


# ---------------------------------------------
def start_process(ssh_session=None):
    return process(BINARY_PATH)


def main():
    if USE_SSH:
        log.info("Connecting via SSH...")
        s = ssh(host=HOST, user=CHALLENGE_NAME, password=PASSWORD, port=PORT)
        p = start_process(s)
    else:
        log.info("Running binary locally...")
        p = start_process()

    # ---------------- EXPLOIT GOES HERE ----------------
    payload = b'A' * 32
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
