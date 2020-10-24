<h1 id='contents'>Table of Contents</h1>

- [FOLDER AND FILES](#folder-and-files)
- [DOCKER](#docker)
  - [Docker File](#docker-file)
  - [requirements.txt](#requirementstxt)
  - [Build Docker Image](#build-docker-image)
  - [Docker Compose](#docker-compose)
    - [Docker Compose Build](#docker-compose-build)
  - [Run Commands](#run-commands)
- [TRAVIS CI](#travis-ci)
  - [Config File](#config-file)
- [FLAKE8](#flake8)
- [DJANGO REST_FRAMEWORK](#django-rest_framework)

# FOLDER AND FILES

[Go Back to Contents](#contents)

- before we start, create the following files

  ```Bash
    touch Dockerfile requirements.txt app docker-compose.yml
  ```

# DOCKER

## Docker File

[Go Back to Contents](#contents)

- in `Dockerfile`

  1. The first line of the file is the image that we want to inherit the file from

     - Search a `Python` image, `3.9-alpine` at [https://hub.docker.com/](https://hub.docker.com/)

       ```Python
         FROM python:3.9-alpine
         # alpine means that is light version of docker and runs python 3.9
       ```

  2. The second line is the maintainer name, this is optional

     ```Python
       LABEL maintainer="Roger Takeshita"
     ```

  3. The third line we define the python unbuffered variable

     ```Python
       # To define an environment variable, just define `ENV NAME_OF_THE_VARIABLE VALUE`
       # This tells python to run in unbuffered mode. Which is recommended when we are running python in a Docker Container. This avoids complications with the python outputs while using inside a docker
       # This prints directly the output, instead of buffered.
       ENV PYTHONUNBUFFERED 1
     ```

  4. Install the requirements.txt
     ```Python
       # COPY The_project_requirements  and copy into docker_image_requirements
       COPY ./requirements.txt /requirements.txt
     ```
  5. Install the requirements.txt into docker image

     ```Python
       RUN pip install -r /requirements.txt
     ```

  6. Create a directory inside our image to store our application

     ```Python
        # Create the app folder
        RUN mkdir /app
        # Then we set the default directory of our app
        WORKDIR /app
        # Copy our app into docker app
        COPY ./app /app
     ```

  7. Create a user that is going to run our docker application

     - We do that for security purposes, if we don't define that, the image will run the application with the root account

     ```Python
       RUN adduser -D user
       # adduser = create user
       # -D      = only for running applications
       # user    = the name of the user
       USER user
       # USER user = Change the user to user
     ```

  ```Python
    FROM python:3.9-alpine
    LABEL maintainer="Roger Takeshita"

    ENV PYTHONUNBUFFERED 1

    COPY ./requirements.txt /requirements.txt

    RUN pip install -r /requirements.txt

    RUN mkdir /app
    WORKDIR /app
    COPY ./app /app

    RUN adduser -D user
    USER user
  ```

## requirements.txt

[Go Back to Contents](#contents)

- in `requirements.txt`

  - We are going to install all packages that we need
  - We can find the package at [https://pypi.org](https://pypi.org)

    ```Txt
      Django>=3.1.2,<3.2.0
      djangorestframework>=3.12.1,<3.20.0
    ```

## Build Docker Image

[Go Back to Contents](#contents)

- on your projects folder, run

  ```Bash
    docker build .
  ```

## Docker Compose

[Go Back to Contents](#contents)

- Docker compose configuration for our project
- Docker compose is a tool that helps us to run our docker image easily from our project location
- in `docker-compose.yml`

  ```Python
    # First line, docker version that we are going to sue
    version: "3"
    # Next we define the services of our application
    services:
      # we only have one service called app
      app:
        # this means that our build section of the configuration, we define de context ., this means that is the main folder of our project
        build:
          context: .
        # port configuration, we are going to map our project on port 8000 and on our image on port 8000
        # "project_port:image_port"
        ports:
          - "8000:8000"
        # volume allows us to get the updates from our project into the docker image
        # it will map our ./app directory in our project into /app directory in our docker image
        volumes:
          - ./app:/app
        # the commando to run our application in our docker image container
        command: >
          sh -c "python manage.py runserver 0.0.0.0:8000"
          # sh = means shell
          # -c = run command
  ```

  ```Python
    version: "3"

    services:
      app:
        build:
          context: .
        ports:
          - "8000:8000"
        volumes:
          - ./app:/app
        command:
          sh -c "python manage.py runserver 0.0.0.0:8000"
  ```

### Docker Compose Build

[Go Back to Contents](#contents)

- Run the following command to build a docker image with our docker compose configuration

  ```Bash
    docker-compose build
  ```

## Run Commands

[Go Back to Contents](#contents)

- To run the commands using docker

  ```Bash
    docker-compose run app sh -c "django-admin.py startproject config ."

    # docker-compose run                      = docker command to run command
    # app                                     = the name of our service
    # sh -c                                   = shell command
    # "django-admin.py startproject config ." = the command
  ```

  - Because we defined the `WORKDIR` in our docker compose and changed the dir into that folder
  - Docker will create our project inside the `WORKDIR`

# TRAVIS CI

[Go Back to Contents](#contents)

- [Travis CI Website](https://travis-ci.org/)
- Travis CI is a hosted continuous integration service used to build and test software projects hosted at GitHub and Bitbucket. Travis CI provides various paid plans for private projects, and a free plan for open source.

## Config File

[Go Back to Contents](#contents)

- Create `.travis.yml` on the root of the project

  ```Bash
    touch .travis.yml app/.flake8
  ```

# FLAKE8

[Go Back to Contents](#contents)

- Flake8. Which is “the wrapper which verifies pep8, pyflakes and circular complexity
- in `app/.flake8`

  ```Bash
    [flake8]
    exclude =
      migrations,
      __pycache__,
      manage.py,
      settings.py
  ```

# DJANGO REST_FRAMEWORK

[Go Back to Contents](#contents)
