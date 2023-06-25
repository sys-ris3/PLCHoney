import os, time

while True:
    try:
        procs = os.popen('ps -elf | grep honeypot_proxy | grep -v grep').read()
        target_pid = procs.split()[3]

        print("Terminating", target_pid)
        os.system("kill -9 "+str(target_pid))

        time.sleep(0.1)
    except:
        print("All proxy server instances stopped.")
        break
