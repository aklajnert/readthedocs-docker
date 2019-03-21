import os
import subprocess
import sys



def run_command(command, shell = False):
    cmd = command.split() if isinstance(command, str) or not shell else command

    process = subprocess.Popen(cmd, shell=shell)
    process.wait()

    if process.returncode != 0:
        sys.exit(f"Command failed: {command}")


def main():
    os.execvp('python3.6', ['python3.6', 'manage.py', 'runserver'])


if __name__ == "__main__":
    main()
