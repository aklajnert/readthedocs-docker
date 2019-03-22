FROM python:3.6.8-alpine3.9

RUN apk update && apk add git g++ gcc libxslt-dev uwsgi uwsgi-python3

RUN git clone --recurse-submodules https://github.com/rtfd/readthedocs.org.git

WORKDIR readthedocs.org
RUN pip install -r requirements.txt

RUN python manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')", | python manage.py shell
RUN python manage.py collectstatic

COPY uwsgi.ini /etc/uwsgi.ini

EXPOSE 8000
ENTRYPOINT ["uwsgi", "--ini", "/etc/uwsgi.ini"]
