import logging
import os
import time

import psutil

log = logging.getLogger("codi-app ({})".format(__name__))
log.setLevel(logging.DEBUG)


def check_and_kill(file):
    pid = None
    try:
        f = open(file, "r")
        pidstr = f.read()
        f.close()
        pid = int(pidstr)
    except Exception as e:
        return False

    log.info("Shutting down `codi-app` related processes..")
    log.debug("PID: {}".format(pid))
    count = 0
    while pid > 0 and psutil.pid_exists(pid):
        try:
            os.kill(pid, count)
            if count == 9:
                os.waitpid(pid, 0)
            count = count + 1
            time.sleep(1)
            log.debug("Killed PID: {}".format(pid))
            print("killed", count)
        except OSError:
            log.error(
                "Couldn't deliver signal (count: {}), to PID: {}".format(count, pid)
            )
            pid = 0
    os.remove(file)
    return count > 0


def lock(file):
    pidfd = os.open(file, os.O_CREAT | os.O_WRONLY | os.O_EXCL)
    os.write(pidfd, str(os.getpid()).encode())
    os.close(pidfd)


def remove(file):
    log.debug("Removed pidfile: {}".format(file))
    os.remove(file)
