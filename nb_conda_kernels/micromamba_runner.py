import os
import shlex
import sys


def exec_in_env(micromamba, env_path, *command):
    if sys.platform.startswith("win"):
        # NOTE: Windows is untested
        ecomm = [
            micromamba,
            "{} run -p {} {}".format(micromamba, env_path, shlex.join(command)),
        ]
    else:
        # NOTE: this works around a bug in `micromamba run` where signals are
        # not forwarded to child processes on Linux.  This leads to orphaned
        # IPython kernel processes.
        #
        # See this issue for more information:
        #    https://github.com/mamba-org/mamba/issues/1820
        shellhook = "eval \"$('{micromamba}' shell hook -s bash)\"".format(
            micromamba=micromamba
        )
        activate = ["micromamba", "activate", env_path]
        ecomm = "{shellhook} && {activate} && exec {command}".format(
            shellhook=shellhook,
            activate=shlex.join(activate),
            command=shlex.join(command),
        )
        ecomm = ["bash", "-c", ecomm]
    os.execvp(ecomm[0], ecomm)


if __name__ == "__main__":
    exec_in_env(*(sys.argv[1:]))
