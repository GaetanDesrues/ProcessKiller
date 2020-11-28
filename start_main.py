import os
import signal
import subprocess
import sys
import time
from os.path import join

# known_location
PIDS_DIR = join("/tmp", "tmp.known_location")
# task identifiers
keys = ["my_task_1", "my_task_2"]


class Main:
    def __init__(self):
        # retrieve processes from files
        self.pids = get_pids()

        # setup signal handler
        signal.signal(signal.SIGINT, self.sign_callback())

        # print processes
        see_processes()

    def sign_callback(self):
        def signal_handler(sig, frame):
            print(f" : Main.sign_callback   (from {os.getpid()})")
            self.cleanup()
            sys.exit("\nProgram stopped. Ok")

        return signal_handler

    def cleanup(self):
        for k, v in self.pids.items():
            # kill processes
            for p in v["ps"]:
                try:
                    os.kill(p, signal.SIGKILL)
                    print(f"{k}: {p} was killed")
                except ProcessLookupError as e:
                    # silent error
                    print(f"{k}: pid={p} -- {e}")

            # # delete files
            # if os.path.isfile(v["fname"]):
            #     os.remove(v["fname"])


    def do_something(self):
        time.sleep(20)


def get_pids():
    pids = {}
    # retrieve processes with task identifiers
    for k in keys:
        pids[k] = {}
        fname = join(PIDS_DIR, f"{k}.pid")
        with open(fname, "r") as f:
            pids[k].update(
                {
                    # list of processes in the file
                    "ps": list(map(int, [x.rstrip() for x in f.readlines()])),
                    # file path
                    "fname": fname,
                }
            )

    print("\n --- PIDs:", flush=True)
    for k, v in pids.items():
        print(f"{k}: {', '.join(map(str, v['ps']))}.")

    return pids


def see_processes():
    ps = subprocess.Popen(("ps", "-e"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("grep", "python"), stdin=ps.stdout)
    ps.wait()
    print(f"\n --- Processes:\n{output.decode('utf-8')}\n")


if __name__ == "__main__":
    mm = Main()
    mm.do_something()
