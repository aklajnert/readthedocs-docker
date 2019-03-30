# readthedocs-docker

Docker image to run readthedocs.org on-premise.

## Build image

```bash
docker build -t readthedocs .
```

## Running application

The recommended approach is to use `docker-compose`. It contains full stack necessary to
run `readthedocs.org` app including `PostgresSQL` database, `Redis` and the application itself.

Simply run `docker compose up`, and application will start.

The admin account is created only on first startup when database is empty and `RTD_ADMIN_USERNAME` 
environment variable is set. The password is autogenerated, it will appear only once in the log.
Look for a following message in web application logs:  
```
Created admin account with username: "rtd-admin" and password: "<random-pass>". Save the password somewhere, as it won't appear again.
```

Save the password, or change it because as the message says - it won't appear again.

