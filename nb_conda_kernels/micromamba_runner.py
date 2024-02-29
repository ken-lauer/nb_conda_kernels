import os
import shlex
import sys


def exec_in_env(micromamba, env_path, *command):
    ecomm = "{} run -p {} {}".format(micromamba, env_path, shlex.join(command))
    print(ecomm)
    ecomm = ['bash', '-c', ecomm]
    os.execvp(ecomm[0], ecomm)


if __name__ == '__main__':
    exec_in_env(*(sys.argv[1:]))
