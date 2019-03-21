import os
import subprocess
import sys

RUN_MIGRATIONS = not bool(os.environ.get('RTD_DISABLE_MIGRATIONS', False))


def run_command(command, shell = False):
    cmd = command.split() if isinstance(command, str) or not shell else command

    process = subprocess.Popen(cmd, shell=shell)
    process.wait()

    if process.returncode != 0:
        sys.exit(f"Command failed: {command}")


def main():
    if RUN_MIGRATIONS:
        run_command('python manage.py migrate')

    run_command(
        'echo "from django.contrib.auth import get_user_model; User = get_user_model(); '
        'User.objects.create_superuser(\'admin\', \'admin@myproject.com\', \'password\')", | '
        'python manage.py shell')


if __name__ == "__main__":
    main()
