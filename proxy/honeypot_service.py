import os, time

required_dirs = ['logs', 'errors']
for dir in required_dirs:
    if os.path.exists(dir) == False:
        os.mkdir(dir)

while True:
    log_index = len(os.listdir('logs'))
    error_index = len(os.listdir('errors'))

    print("Running server iteration "+str(log_index))

    os.system('python3 honeypot_proxy.py >> ./logs/proxy_log_'+str(log_index)+'.log 2>> ./errors/proxy_error_'+str(error_index)+'.err')

    os.system('python3 stop_proxy.py')
    time.sleep(1)
