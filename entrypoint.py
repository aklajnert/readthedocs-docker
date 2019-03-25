import os
import subprocess
# import uuid

from django.conf import settings
# from django.contrib.auth import get_user_model


def main():
    import django

    django.setup()

    migrate = ("python", "manage.py", "migrate")
    assert subprocess.call(migrate) == 0, "Database sync failed"
    collect_static = ("python", "manage.py", "collectstatic", "--noinput", "--clear", "-v", "0")
    assert subprocess.call(collect_static) == 0, "Collect static job failed"

    # admin_username = os.environ.get('RTD_ADMIN_USERNAME')
    # admin_email = os.environ.get('RTD_ADMIN_EMAIL', 'rtd-admin@example.com')

    # if admin_username:
    #     if not User.objects.filter(username=admin_username).exists():
    #         password = uuid.uuid4()
    #         User.create_superuser(admin_username, admin_email, password)
    #         print(f'Created admin account with username {admin_username} and password: "{password}"')

    os.execvp("uwsgi", ["uwsgi", "--ini", "/etc/uwsgi.ini"])


if __name__ == "__main__":
    main()
