# Overview

This project provides a solution to generate a .htpasswd file on the fly and serve it using Docker Compose. This setup is particularly useful for integrating basic authentication into services like Nginx by utilizing Docker containers. The project leverages a Python script to create the .htpasswd file and Docker Compose to manage the containers.

## Python file
### Help
```
λ python generator.py -h
usage: generator.py [-h] [-f FILE_NAME] [-u USER] [-p PASSWORD] [-ph PATH]

Configure the .htpasswd file

options:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file-name FILE_NAME
                        Name of the file. Default is '.htpasswd'
  -u USER, --user USER  The user for authentication
  -p PASSWORD, --password PASSWORD
                        The password for authentication
  -ph PATH, --path PATH
                        The path where the file will be generated. Default is '/'
```

### Example with docker-compose.yml
In this example the username is `admin` and password is `123admin`. 
```
version: '3.7'

services:

  htpasswd:
    image: sofocused/htpasswd:1.0
    command: >
      sh -c "python generator.py -u admin -p 123admin --path /htpasswd && tail -f /dev/null"
    volumes:
      - htpasswd:/app/htpasswd/

  frontend:
    build:
      context: .
    restart: always
    depends_on:
      - htpasswd
    ports:
      - "80:80"
    volumes:
      - htpasswd:/etc/nginx/htpasswd

volumes:
  htpasswd: {}
```

Now in your nginx conf file
```
...

# Prometheus
location /prometheus/ {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/htpasswd/.htpasswd;

    proxy_pass http://prometheus-service:9090/;
}

...
```

# TODO
Reduce image size


