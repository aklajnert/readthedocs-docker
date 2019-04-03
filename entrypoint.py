import os
import secrets
import subprocess

from django.conf import settings
from django.contrib.auth import get_user_model


def main():
    import django

    django.setup()

    User = get_user_model()

    migrate = ("python", "manage.py", "migrate")
    assert subprocess.call(migrate) == 0, "Database sync failed"
    collect_static = ("python", "manage.py", "collectstatic", "--noinput", "--clear", "-v", "0")
    assert subprocess.call(collect_static) == 0, "Collect static job failed"

    if not User.objects.filter(username=settings.SLUMBER_USERNAME):
        User.objects.create_superuser(username=settings.SLUMBER_USERNAME,
                                      password=settings.SLUMBER_PASSWORD,
                                      email='slumber@example.com')
        print('Created slumber user.')

    admin_username = os.environ.get("RTD_ADMIN_USERNAME")
    admin_email = os.environ.get("RTD_ADMIN_EMAIL", "rtd-admin@example.com")

    if admin_username:
        from allauth.account.models import EmailAddress
        if not User.objects.filter(username=admin_username).exists():
            password = secrets.token_hex(16)
            user = User.objects.create_superuser(admin_username, admin_email, password)
            print(
                f'Created admin account with username: "{admin_username}" and password: "{password}". '
                f'Save the password somewhere, as it won\'t appear again.'
            )

            EmailAddress.objects.create(user=user, email=admin_email, primary=True, verified=True)

        else:
            print(f'Admin account {admin_username} already exist.')

    os.execvp("uwsgi", ["uwsgi", "--ini", "/etc/uwsgi.ini"])


if __name__ == "__main__":
    main()
