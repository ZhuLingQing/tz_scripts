import os, sys, time

def lookfor_lxssmanager():
    cmd_tasklist = "tasklist /svc /fi \"services eq LxssManager\"" 
    out = os.popen(cmd_tasklist)
    r = out.readlines()
    if len(r) < 4:
        return None
    if r[3].find('svchost.exe') < 0: return None
    pid =  ' '.join(r[3].split()).split()[1]
    print(f"LxssManager: {pid}")
    return int(pid)

if "__main__" == __name__:
    while True:
        pid = lookfor_lxssmanager()
        if None == pid: break
        cmd_delete = f"wmic process where processid={pid} delete"
        out = os.popen(cmd_delete)
    cmd_start = "sc start LxssManager"
    out = os.popen(cmd_start)
    time.sleep(1)
    pid = lookfor_lxssmanager()
    if None == pid: print("lxssmanager not launched")
    else: print("lxssmanager launch success")
    print("DONE")