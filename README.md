<h1 id='contents'>Table of Contents</h1>

- [FOLDER AND FILES](#folder-and-files)
  - [Postman](#postman)
- [DOCKER](#docker)
  - [Docker File](#docker-file)
  - [requirements.txt](#requirementstxt)
  - [Build Docker Image](#build-docker-image)
  - [Docker Compose](#docker-compose)
    - [Start Server](#start-server)
    - [Docker Compose Build](#docker-compose-build)
- [DJANGO REST_FRAMEWORK](#django-rest_framework)
  - [Enable Travis CI and Flake8](#enable-travis-ci-and-flake8)
    - [Travis CI](#travis-ci)
      - [Config .travis.yml](#config-travisyml)
    - [Flake8](#flake8)
      - [Config Flake8](#config-flake8)
  - [Start New Project Using Docker](#start-new-project-using-docker)
    - [Create a New App Using Docker](#create-a-new-app-using-docker)
  - [Core App](#core-app)
    - [Create Folder and Files](#create-folder-and-files)
    - [Settings.py](#settingspy)
    - [Project Urls](#project-urls)
    - [Model](#model)
      - [BaseUserManager](#baseusermanager)
      - [AbstractBaseUser](#abstractbaseuser)
      - [PermissionsMixin](#permissionsmixin)
    - [Config Auth Settings](#config-auth-settings)
    - [Migrations](#migrations)
      - [Makemigrations](#makemigrations)
      - [Migrate](#migrate)
    - [Admin Panel](#admin-panel)
    - [Management Commands](#management-commands)
    - [Create Superuser](#create-superuser)
    - [Core - Tests](#core---tests)
      - [Mocking](#mocking)
        - [PATCH()](#patch)
        - [MANAGEMENT COMMANDS](#management-commands-1)
  - [User App](#user-app)
    - [User - Folder and Files](#user---folder-and-files)
    - [User - Register New App](#user---register-new-app)
    - [User - Serializers](#user---serializers)
    - [User - View (Controllers)](#user---view-controllers)
    - [User - Urls (Routes)](#user---urls-routes)
    - [User - Register Base API Url](#user---register-base-api-url)
    - [User - Token Authentication](#user---token-authentication)
    - [User - Manage Endpoints](#user---manage-endpoints)
    - [User - Tests](#user---tests)
  - [Recipe APP](#recipe-app)
    - [Recipe - Create New App](#recipe---create-new-app)
    - [Recipe - Folder and Files](#recipe---folder-and-files)
    - [Recipe - Register a New App](#recipe---register-a-new-app)
    - [Recipe - Register Base API Url](#recipe---register-base-api-url)
    - [Tag](#tag)
      - [Tag - Models](#tag---models)
      - [Tag - Migrations](#tag---migrations)
      - [Tag - Register App Admin Panel](#tag---register-app-admin-panel)
      - [Tag - Serializer](#tag---serializer)
      - [Tag - Views](#tag---views)
      - [Tag - Urls (Router)](#tag---urls-router)
      - [Tag - Test Model](#tag---test-model)
      - [Tag - Tests](#tag---tests)
    - [Ingredient](#ingredient)
      - [Ingredient - Folder and Files](#ingredient---folder-and-files)
      - [Ingredient - Models](#ingredient---models)
      - [Ingredient - Migrations](#ingredient---migrations)
      - [Ingredient - Register App Admin Panel](#ingredient---register-app-admin-panel)
      - [Ingredient - Serializer](#ingredient---serializer)
      - [Ingredient - Views](#ingredient---views)
      - [Ingredient - Urls (Router)](#ingredient---urls-router)
      - [Ingredient - Test Models](#ingredient---test-models)
      - [Ingredient - Test](#ingredient---test)
    - [Recipe - REFACTOR View (Controller)](#recipe---refactor-view-controller)
    - [Recipe](#recipe)
      - [Recipe - Folder and Files](#recipe---folder-and-files-1)
      - [Recipe - Model](#recipe---model)
      - [Recipe - Migrations](#recipe---migrations)
      - [Recipe - Register App Admin Panel](#recipe---register-app-admin-panel)
      - [Recipe - Serializer](#recipe---serializer)
      - [Recipe - Views (Controllers)](#recipe---views-controllers)
      - [Recipe - Urls (Router)](#recipe---urls-router)
      - [Recipe - Test Models](#recipe---test-models)
      - [Recipe - Test](#recipe---test)
        - [RECIPE - IMAGE UPLOAD TEST](#recipe---image-upload-test)
      - [Recipe - Filter](#recipe---filter)
        - [RECIPE - VIEWS (CONTROLLERS)](#recipe---views-controllers-1)
        - [RECIPE - TEST FILTER](#recipe---test-filter)
        - [TAG - TEST FILTER](#tag---test-filter)
        - [INGREDIENT - TEST FILTER](#ingredient---test-filter)

# FOLDER AND FILES

[Go Back to Contents](#contents)

- before we start, create the following files

  ```Bash
    touch Dockerfile requirements.txt app docker-compose.yml
  ```

## Postman

[Go Back to Contents](#contents)

- [Postman API Calls](https://github.com/Roger-Takeshita/Django_REST_Framework/blob/master/Django_Rest_Framework_Recipes.postman_collection.json)

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
       RUN apk add --update --no-cache postgresql-client jpeg-dev
       # apk        = uses the package management tha comes with python 3.9-alpine
       # add        = add a package
       # --update   = update the package
       # --no-cache = don't install/cache the apk registry in our docker file (to minimize the size of packages/files included in our dockerfile)
       # postgresql-client = dependency to use PostgreSQL
       # jpeg-dev = adds jpeg binary to our docker file for Pillow (PIL)
       RUN apk add --update --no-cache --virtual .tmp-build-deps \
           gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
       # postgreSQL dependencies/requirements, create a temporary virtual folder to install and then remove after the installation
       # postgresql-dev = build dependency for PostgreSQL
       # musl-dev zlib zlib-dev = build dependency for Pillow (PIL)
       RUN pip install -r /requirements.txt
       RUN apk del .tmp-build-deps
       # Deletes the temporary virtual folder
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

  7. Create **media** and **static** folder

  ```Python
    RUN mkdir -p /vol/web/media
    RUN mkdir -p /vol/web/static
  ```

  8. Create a user that is going to run our docker application

     - We do that for security purposes, if we don't define that, the image will run the application with the root account

     ```Python
       RUN adduser -D dockeruser
       # adduser               = create a user
       # -D                    = only for running applications
       # dockeruser            = the name of the user
       RUN chown -R dockeruser:dockeruser /vol
       # chown                 = Change the owner of the folder
       # -R                    = Recursively
       # dockeruser:dockeruser = To dockeruser
       RUN chmod -R 755 /vol/web
       # chmod                 = Change folder mod
       # -R                    = Recursively
       # 755                   = Owner can Read/Write
       # /vol/web              = Folder path
       USER dockeruser
       # USER dockeruser       = Change the user to dockeruser
     ```

  ```Python
    FROM python:3.9-alpine
    LABEL maintainer="Roger Takeshita"

    ENV PYTHONUNBUFFERED 1

    COPY ./requirements.txt /requirements.txt
    RUN apk add --update --no-cache postgresql-client jpeg-dev
    RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
    RUN pip install -r /requirements.txt
    RUN apk del .tmp-build-deps

    RUN mkdir /app
    WORKDIR /app
    COPY ./app /app

    RUN mkdir -p /vol/web/media
    RUN mkdir -p /vol/web/static

    RUN adduser -D dockeruser
    RUN chown -R user:dockeruser /vol/
    RUN chmod -R 755 /vol/web
    USER dockeruser
  ```

## requirements.txt

[Go Back to Contents](#contents)

- in `requirements.txt`

  - We are going to install all packages that we need
  - We can find the package at [https://pypi.org](https://pypi.org)

    - [Pillow - PIL - Upload Images](https://pillow.readthedocs.io/en/stable/index.html)
      - This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.
    - [psycopg2 - PostgreSQL Adapter](https://pypi.org/project/psycopg2/)
      - Psycopg is the most popular PostgreSQL database adapter for the Python programming language.
    - [flake8](https://flake8.pycqa.org/en/latest/)
      - flake8 is a command-line utility for enforcing style consistency across Python projects. By default it includes lint checks provided by the PyFlakes project, PEP-0008 inspired style checks provided by the PyCodeStyle project, and McCabe complexity checking provided by the McCabe project.

    ```Txt
      Django>=3.1.2,<3.2.0
      djangorestframework>=3.12.1,<3.20.0
      flake8>=3.8.4,<3.9.0
      psycopg2>=2.8.6,<2.9.0
      Pillow>=8.0.1,<8.1.0
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
      # create our app service
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
          sh -c "python manage.py wait_for_db &&
                # starts our custom wait_for_db file, this step is necessary to avoid starting the server without the database is ready
                python manage.py migrate &&
                # create our migrations, to avoid errors
                python manage.py runserver 0.0.0.0:8000"
                # start the server
          # sh = means shell
          # -c = run command
        environment:
          # environment variables to connect to our database
          - DB_HOST=db
          - DB_NAME=app
          - DB_USER=postgres
          - DB_PASS=supersecretpassword
        depends_on:
          # depends_on means that db will start before the app
          - db
      # create our db service
      db:
        # using a light version of postgreSQL
        image: postgres:10-alpine
        # environment variables to create database, username and password
        environment:
          - POSTGRES_DB=app
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=supersecretpassword
          # the password in this case is not super import, but if you are running a production built, you should use the Travis-CI environment variable, this way you password is not public
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
        command: >
          sh -c "python manage.py wait_for_db &&
                 python manage.py migrate &&
                 python manage.py runserver 0.0.0.0:8000"
        environment:
          - DB_HOST=db
          - DB_NAME=app
          - DB_USER=postgres
          - DB_PASS=supersecretpassword
        depends_on:
          - db
      db:
        image: postgres:10-alpine
        environment:
          - POSTGRES_DB=app
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=supersecretpassword
  ```

### Start Server

[Go Back to Contents](#contents)

- To start the docker server

  - This command will start our server using the `docker-compose.yml` configuration

    ```Bash
      docker-compose up
    ```

  - This command will output something like:

    ```Bash
      app_1  | Django version 3.1.2, using settings 'config.settings'
      app_1  | Starting development server at http://0.0.0.0:8000/
      app_1  | Quit the server with CONTROL-C.
    ```

    - We are not going to use the `http://0.0.0.0:8000/` to connect to our app
    - Because we configured to use our localhost on port `8000` and then forward to our docker port `8000`
    - We need to use [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Docker Compose Build

[Go Back to Contents](#contents)

- Run the following command to build a docker image with our docker compose configuration

  ```Bash
    docker-compose build
  ```

# DJANGO REST_FRAMEWORK

[Go Back to Contents](#contents)

## Enable Travis CI and Flake8

### Travis CI

[Go Back to Contents](#contents)

- [Travis CI Website](https://travis-ci.org/)
- [Travis CI Tutorial](https://docs.travis-ci.com/user/tutorial/)
- [Travis CI - Project Build](https://travis-ci.org/github/Roger-Takeshita/Django_REST_Framework)
- Travis CI is a hosted continuous integration service used to build and test software projects hosted at GitHub and Bitbucket. Travis CI provides various paid plans for private projects, and a free plan for open source.

#### Config .travis.yml

[Go Back to Contents](#contents)

- Create `.travis.yml` on the root of the project

  ```Bash
    touch .travis.yml app/.flake8
  ```

### Flake8

[Go Back to Contents](#contents)

- Flake8. Which is:
  > the wrapper which verifies pep8, pyflakes and circular complexity

#### Config Flake8

[Go Back to Contents](#contents)

- in `app/.flake8`

  - we are going to exclude some files

    ```Bash
      [flake8]
      exclude =
        migrations,
        __pycache__,
        manage.py,
        settings.py
    ```

## Start New Project Using Docker

[Go Back to Contents](#contents)

- Run the following command to start a new project in docker

  ```Bash
    docker-compose run --rm app sh -c "django-admin.py startproject config ."

    # docker-compose run                      = docker command to run command
    # --rm                                    = removes the previous app
    # app                                     = the name of our service
    # sh -c                                   = shell command
    # "django-admin.py startproject config ." = the command
  ```

  - Because we defined the `WORKDIR` in our docker compose and changed the dir into that folder
  - Docker will create our project inside the `WORKDIR`

### Create a New App Using Docker

[Go Back to Contents](#contents)

- Run the following command to start a new app in docker

  ```Bash
    docker-compose run --rm app sh -c "python manager.py startapp core"

    # docker-compose run                = docker command to run command
    # --rm                              = removes the previous app
    # app                               = the name of our service
    # sh -c                             = shell command
    # "python manager.py startapp core" = the command
  ```

  - Because we defined the `WORKDIR` in our docker compose and changed the dir into that folder
  - Docker will create our app inside the `WORKDIR`

- Delete `app/core/tests.py` and `app/core/views.py`, since we are not going to be using

  ```Bash
    .
    ├── app
    │   ├── __pycache__
    │   ├── config
    │   │   ├── __pycache__
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── core
    │   │   ├── __pycache__
    │   │   ├── migrations
    │   │   │   ├── __pycache__
    │   │   │   └── __init__.py
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── tests.py            <--- Delete
    │   │   └── views.py            <--- Delete
    │   ├── .flake8
    │   ├── db.sqlite3
    │   └── manage.py
    ├── .gitignore
    ├── .travis.yml
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    └── requirements.txt
  ```

## Core App

### Create Folder and Files

[Go Back to Contents](#contents)

- Create the following files using my custom [touch](https://github.com/Roger-Takeshita/Shell-Script/blob/master/touch-open.sh) command

  ```Bash
    touch app/core/tests/__init__.py + test_models.py app/core/management/__init__.py + wait_for_db.py
  ```

### Settings.py

[Go Back to Contents](#contents)

- After creating a new app we need to register this app
- in `app/config/settings.py`

  - Import the `os`, so we can import the environment variables that we defined in our `docker-compose.yml`
  - Add our new app (`core`) into the **INSTALLED_APPS** array
  - Add **rest_framework**, responsible for creating our REST APIs
  - Add **rest_framework.authtoken**, responsible for creating authentication tokens

    ```Python
      INSTALLED_APPS = [
          'core',
          'rest_framework',
          'rest_framework.authtoken',
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',
      ]
    ```

  - Update the database information to use postgreSQL

    ```Python
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'HOST': os.environ.get('DB_HOST'),
              'NAME': os.environ.get('DB_NAME'),
              'USER': os.environ.get('DB_USER'),
              'PASSWORD': os.environ.get('DB_PASS'),
          }
      }
    ```

  - Setup the **media** and **static** folder and roots

    ```Python
      STATIC_URL = '/static/'
      MEDIA_URL = '/media/'

      MEDIA_ROOT = '/vol/web/media'
      STATIC_ROOT = '/vol/web/static'
    ```

  - Add the auth model

    ```Python
      AUTH_USER_MODEL = 'core.User'
      # Configure our app to use authentication using the following table
      # core    = the name of the app
      # User    = the table
    ```

  ```Python
    from pathlib import Path
    import os

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = "$+5x9n2g=vg2s4_yluxv_0cjg7wibx#sf%ov%p*jq%2txjj%@e"

    DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'core',
        'rest_framework',
        'rest_framework.authtoken',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'config.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'config.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ.get('DB_HOST'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    MEDIA_ROOT = '/vol/web/media'
    STATIC_ROOT = '/vol/web/static'

    AUTH_USER_MODEL = 'core.User'
  ```

### Project Urls

[Go Back to Contents](#contents)

- in `app/config/urls.py`

  - The following steps are only required if you are going to use Pillow (PIL) and local media storage
    - import **static** from `django.conf.urls.static`
    - import **settings** from `django.conf`
    - in the end of the urlpattern add ` + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
      - To set the path to our images

  ```Python
    from django.contrib import admin
    from django.urls import path
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        path('admin/', admin.site.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

### Model

[Go Back to Contents](#contents)

- In `app/core/models.py`

  - We are going to create our user model

    ```Python
      from django.db import models
      from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

      # The UserManager class provide us a helper function to create a user or create a super user
      # We inherit the BaseUserManager, all the features tha comes with the base user manager, but we are going to override some functions to handle our email address instead of the username (default)
      class UserManager(BaseUserManager):
          def create_user(self, email, password=None, **extra_fields):
              # **extra_fields, just like in JS, all the rest of the fields will be passed to extra_fields
              """
              Creates and save a new user
              """
              # Checks if the email is valid/not empty
              if not email:
                  raise ValueError('Users must have an email address.')
              # Create a new user using - self.model() shorthand
              # self.normalize_email() is a helper method from BaseUserManager that allow us to normalize the email
              # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email
              user = self.model(email=self.normalize_email(email), **extra_fields)
              # use the set_password helper function that comes with AbstractBaseUser to hash the password
              user.set_password(password)
              # using=self._db is only required when we are using multiple databases. But it's a good practice to add it anyway
              user.save(using=self._db)

              return user

          # Create superuser function
          def create_superuser(self, email, password):
              """Creates and saves a new super user"""
              # Uses the method that we already created to create a normal user
              user = self.create_user(email, password)
              user.is_superuser = True
              user.is_staff = True
              user.save(using=self._db)

              return user

      # Create our user model and we are going to extend from AbstractBaseUser, PermissionsMixin
      class User(AbstractBaseUser, PermissionsMixin):
          """
          Custom user model that suppors using email instead username
          """
          email = models.EmailField(max_length=255, unique=True)
          name = models.CharField(max_length=255)
          is_active = models.BooleanField(default=True)
          is_staff = models.BooleanField(default=False)

          # Then we assign the objects to the UserManager()
          objects = UserManager()

          # then we change the default username to email
          USERNAME_FIELD = 'email'
    ```

#### BaseUserManager

[Go Back to Contents](#contents)

- **[BaseUserManager](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager)** You should also define a custom manager for your user model. If your user model defines `username`, `email`, `is_staff`, `is_active`, `is_superuser`, `last_login`, and `date_joined` fields the same as Django’s default user, you can install Django’s UserManager; however, if your user model defines different fields, you’ll need to define a custom manager that extends `BaseUserManager` providing two additional methods:

  - **create_user(username_field, password=None, \*\*other_fields)**

    - The prototype of `create_user()` should accept the username field, plus all required fields as arguments. For example, if your user model uses `email` as the username field, and has `date_of_birth` as a required field, then `create_user` should be defined as:

      ```Python
        def create_user(self, email, date_of_birth, password=None):
        # create user here
        ...
      ```

  - **create_superuser(username_field, password=None, \*\*other_fields)**

    - The prototype of `create_superuser()` should accept the username field, plus all required fields as arguments. For example, if your user model uses `email` as the username field, and has `date_of_birth` as a required field, then `create_superuser` should be defined as:

      ```Python
        def create_superuser(self, email, date_of_birth, password=None):
        # create superuser here
        ...
      ```

#### AbstractBaseUser

[Go Back to Contents](#contents)

- **[AbstractBaseUser](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser)** provides the core implementation of a user model, including hashed passwords and tokenized password resets. You must then provide some key implementation details:

  - **USERNAME_FIELD** A string describing the name of the field on the user model that is used as the unique identifier. This will usually be a username of some kind, but it can also be an email address, or any other unique identifier. The field must be unique (i.e., have unique=True set in its definition), unless you use a custom authentication backend that can support non-unique usernames.

    ```Python
      class MyUser(AbstractBaseUser):
      identifier = models.CharField(max_length=40, unique=True)
      ...
      USERNAME_FIELD = 'identifier'
    ```

  - **is_active** A boolean attribute that indicates whether the user is considered “active”. This attribute is provided as an attribute on AbstractBaseUser defaulting to True. How you choose to implement it will depend on the details of your chosen auth backends.
  - **is_staff** Returns True if the user is allowed to have access to the admin site.

#### PermissionsMixin

[Go Back to Contents](#contents)

- **[PermissionsMixin](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin)** (Custom users and permissions) - To make it easy to include Django’s permission framework into your own user class, Django provides `PermissionsMixin`. This is an abstract model you can include in the class hierarchy for your user model, giving you all the methods and database fields necessary to support Django’s permission model.

### Config Auth Settings

[Go Back to Contents](#contents)

- in `app/config/settings.py`

  - At the end of the file add

    ```Bash
      AUTH_USER_MODEL = 'core.User'
      # Configure our app to use authentication using the following table
      # core    = the name of the app
      # User    = the table
    ```

### Migrations

[Go Back to Contents](#contents)

- Migrations are used to update a database's schema (structure) to match the code in the Models.
- Migrations are used to evolve a database over time - as the requirements of the application change. However, they can be "destructive" (cause a loss of data), so be careful with migrations if you're working with an application in production.
- Migrations in Django are just Python files that are created by running a command Django in Terminal.

#### Makemigrations

[Go Back to Contents](#contents)

- The following command creates migration files for all models that have been added or changed since the last migration:

  ```Bash
    docker-compose run --rm app sh -c "python manager.py makemigrations"
  ```

- The output in the terminal informs us that the following migration file was created: `app/core/migrations/0001_initial.py`
- A migrations directory is created for an app the first time you run **makemigrations**.

#### Migrate

[Go Back to Contents](#contents)

- Simply creating migration files does not update the database.
- To synchronize the database's schema with the code in the migration files, we "migrate" using this command:

  ```Bash
    docker-compose run --rm app sh -c "python manager.py migrate"
  ```

### Admin Panel

[Go Back to Contents](#contents)

- in `app/core/admin.py`

  ```Python
    from django.contrib import admin
    # Import the default user admin (UserAdmin)
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    from core import models

    # Create our custom UserAmin and extend from BaseUserAdmin
    # So we can define custom fields on our admin panel
    class UserAdmin(BaseUserAdmin):
        ordering = ['id']
        # The fields to be used in displaying the User model.
        list_display = ['email', 'name']
        fieldsets = (
            (None, {'fields': ('email', 'password')}),
            (_('Personal Info'), {'fields': ('name',)}),
            (_('Permissions'), {
             'fields': ('is_active', 'is_staff', 'is_superuser')}),
            (_('Important dates'), {'fields': ('last_login',)})

        )
        add_fieldsets = (
            (None, {'classes': ('wide',),
                    'fields': ('email', 'password1', 'password2')}),
        )

    # Register the User table with our custom UserAdmin
    admin.site.register(models.User, UserAdmin)
  ```

  - **fieldsets**

    - You can add "sections" to group related information using **fieldsets**
    - For example:

      ```Python
        class BookInstanceAdmin(admin.ModelAdmin):
        list_filter = ('status', 'due_back')

        fieldsets = (
            (None, {
                'fields': ('book', 'imprint', 'id')
            }),
            ('Availability', {
                'fields': ('status', 'due_back')
            }),
        )
      ```

      - The first argument is the **title**, if you don't want to display the title just pass `None` to omit the tittle.
        ![](https://mdn.mozillademos.org/files/14029/admin_improved_bookinstance_detail_sections.png)

  - **add_fieldsets**
    - The `add_fieldsets` class variable is used to define the fields that will be displayed on the create user page.
    - In our case this will allow us to create `email`, `password1`, and `password2`

### Management Commands

[Go Back to Contents](#contents)

- as a django convention, we store all of commands inside of a folder named **management** in our app folder
- [Writing custom django-admin commands](https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/#module-django.core.management)

  ```Python
    import time
    # default python time module to make sleep for a few moments
    from django.db import connections
    # used to test our database connection with the database
    from django.db.utils import OperationalError
    # db operational error
    from django.core.management.base import BaseCommand
    # we need to import the base command so we can create our custom commands


    class Command(BaseCommand):
        """"Django command to pause execution until database is available"""

        def handle(self, *args, **options):
            # the handle function is executed whenever we call this command/file
            # the arguments for handle is self, *args and **options
            self.stdout.write('Waiting for database...')
            # self.stdout.write used to print things on the script
            db_conn = None
            while not db_conn:
                try:
                    db_conn = connections['default']
                    # if we try to set a connection with the database and the data base is not available, this will raise an OperationalError
                except OperationalError:
                    self.stdout.write('Database unavailable, waiting 1 second...')
                    time.sleep(1)
                    # sleep/wait for 1 sec
            self.stdout.write(self.style.SUCCESS('Database available!'))
            # when whe connection is successful
            # self.style.SUCCESS outputs the msg using different color
  ```

### Create Superuser

[Go Back to Contents](#contents)

- On `Terminal`

  ```Bash
    docker-compose run --rm app sh -c "python manage.py createsuperuser"
  ```

### Core - Tests

[Go Back to Contents](#contents)

- To test our application, we need to import **TestCase** from `djando.test`

  - To use the test model we need to create a `test_file_name.py` or a folder called `tests`. We cannot have both on the root of our app.
  - Run the tests
    - `docker-compose run --rm app sh -c "python manage.py test"`

- In `app/core/tests/test_models.py`

  - Import the **TestCase** from `django.test`
  - Bellow that we are going to import the `get_user_model` helper function to import our models. This is recommended because if we change our user model we will need to change all the tests that uses that model
  - Manually managing a user’s password
    - If you’d like to manually authenticate a user by comparing a plain-text password to the hashed password in the database, use the convenience function [check_password()](https://docs.djangoproject.com/en/3.1/topics/auth/passwords/#module-django.contrib.auth.hashers). It takes two arguments: the plain-text password to check, and the full value of a user’s password field in the database to check against, and returns True if they match, False otherwise.

  ```Python
    from django.test import TestCase
    from django.contrib.auth import get_user_model

    def sample_user():
        """Create a sample user"""
        user = {
            "email": "test@test.com",
            "password": "test123",
            "name": "test"
        }
        return get_user_model().objects.create(**user)

    class ModelTests(TestCase):
        def test_create_user_with_email_successful(self):
            """Test creating a new user with an email is successful"""
            email = 'test@test.com'
            password = 'Test123'
            user = get_user_model().objects.create_user(
                email=email,
                password=password
            )
            self.assertEqual(user.email, email)
            self.assertTrue(user.check_password(password))

        def test_new_user_email_normalized(self):
            """Test the email for a new user is normalized"""
            email = 'test@TEST.COM'
            user = get_user_model().objects.create_user(email, 'Test123')
            self.assertEqual(user.email, email.lower())

        def test_new_user_invalid_email(self):
            """Test creating user with no email raises error"""
            with self.assertRaises(ValueError):
                get_user_model().objects.create_user(None, 'Tes123')

        def test_create_new_superuser(self):
            """Test creating a new superuser"""
            email = 'test@test.com'
            password = 'Test123'
            user = get_user_model().objects.create_superuser(email, password)
            self.assertTrue(user.is_superuser)
            self.assertTrue(user.is_staff)

        def test_tag_str(self):
            """Test the tag string representation"""
            tag = models.Tag.objects.create(
                user=sample_user(),
                name="Vegan"
            )
            self.assertEqual(str(tag), tag.name)
  ```

- In `app/core/tests/test_admin.py`

  - Import **[Client](https://docs.djangoproject.com/en/2.2/topics/testing/tools/#overview-and-a-quick-example)** from `django.test`
    - Client allows us to make test requests to our application
  - Import **[reverse](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/)** from `django.urls`
    - reverse allows us to generate urls for our admin page

  ```Python
    from django.test import TestCase, Client
    from django.contrib.auth import get_user_model
    from django.urls import reverse


    class AdminSiteTests(TestCase):
        def setUp(self):
            """setUp function that runs before each test"""
            # ! Add a client variable set to the Client(). So though self
            # ! we can have access to this variable
            self.client = Client()
            # ! create a new superuser and set to admin_user
            self.admin_user = get_user_model().objects.create_superuser(
                email='admin@test.com',
                password='password123'
            )
            # + uses the client helper function (force_login) to login the user
            # + with django authentication
            self.client.force_login(self.admin_user)
            # ! create a normal user
            self.user = get_user_model().objects.create_user(
                email='noral_user@test.com',
                password='password123',
                name='Normal user full name'
            )

        def test_users_listed(self):
            """TEst that users are listed on user page"""
            # {{ app_label }}_{{ model_name }}_changelist, django docs
            # this method will dynamically generate the url for our admin page
            # so we don't need to hard code
            url = reverse('admin:core_user_changelist')
            res = self.client.get(url)
            self.assertContains(res, self.user.name)
            self.assertContains(res, self.user.email)

        def test_user_change_page(self):
            """Test that the user edit page works"""
            # ! url = /admin/core/user/1
            url = reverse('admin:core_user_change', args=[self.user.id])
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)

        def test_create_user_page(self):
            """Test that create user page works"""
            url = reverse('admin:core_user_add')
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)
  ```

#### Mocking

[Go Back to Contents](#contents)

- Change the behavior of dependencies
- Avoids unintended side-effects
- Never depend on external services

  - Can't guarantee they will be available
  - Make tests unpredictable/unreliable

- [Mocking](https://docs.python.org/3/library/unittest.mock.html)
- `unittest.mock` is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions about how they have been used.
- `unittest.mock` provides a core Mock class removing the need to create a host of stubs throughout your test suite. After performing an action, you can make assertions about which methods / attributes were used and arguments they were called with. You can also specify return values and set needed attributes in the normal way.

##### PATCH()

[Go Back to Contents](#contents)

- Additionally, mock provides a `patch()` decorator that handles patching module and class level attributes within the scope of a test, along with sentinel for creating unique objects.
- The patch decorators are used for patching objects only within the scope of the function they decorate. They automatically handle the unpatching for you, even if exceptions are raised. All of these functions can also be used in with statements or as class decorators.

##### MANAGEMENT COMMANDS

[Go Back to Contents](#contents)

- [django.core.management](https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/#module-django.core.management)
- [django.core.management.call_command](https://docs.djangoproject.com/en/3.1/ref/django-admin/#django.core.management.call_command)
- [Django Unittest Wait for Database](https://stackoverflow.com/questions/52621819/django-unit-test-wait-for-database)
- Running management commands inside our source code

  ```Python
    django.core.management.call_command(name, *args, **options)
  ```

- To call a management command from code use `call_command`.

- **name**
  - the name of the command to call or a command object. Passing the name is preferred unless the object is required for testing.
- **\*args**
  - a list of arguments accepted by the command. Arguments are passed to the argument parser, so you can use the same style as you would on the command line. For example, **call_command('flush', '--verbosity=0')**.
- **\*\*options**

  - named options accepted on the command-line. Options are passed to the command without triggering the argument parser, which means you’ll need to pass the correct type. For example, **call_command('flush', verbosity=0)** (zero must be an integer rather than a string).

- Some command options have different names when using `call_command()` instead of **django-admin** or **manage.py**. For example, `django-admin createsuperuser --no-input` translates to `call_command('createsuperuser', interactive=False)`. To find what keyword argument name to use for `call_command()`, check the command’s source code for the dest argument passed to `parser.add_argument()`.

- in `app/core/tests/test_commands.py`

  ```Python
    from unittest.mock import patch
    from django.core.management import call_command
    from django.db.utils import OperationalError
    from django.test import TestCase


    class CommandTests(TestCase):
        def test_wait_for_db_ready(self):
            """Test waiting for db when db is available"""
            with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
                # + The way we test if the database is available in Django is using
                # + django.db.utils.ConnectionHandler, this will try to retreive
                # + the default database __getitem__ is the function that
                # + retrieves the database
                gi.return_value = True
                # + the patch() function returns a mock object where we have
                # + two properties:
                # -     return_value
                # -     call_count
                call_command('wait_for_db')
                # + test our command with call_command
                # + wait_for_db could be any name
                self.assertEqual(gi.call_count, 1)

        @patch('time.sleep', return_value=True)
        # + When we use patch as a decorator
        # + we can mock the return value as the second argument
        def test_wait_for_db(self, ts):
            # + we have to add a second argument even if we are not going to use it
            # + if we don't do that it will give us an error
            # - in this case we are mocking the timer, so we can speed up the test
            """Test waiting for db"""
            with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
                gi.side_effect = [OperationalError] * 5 + [True]
                # + the unittest.mock has side_effect method
                # + we can apply to the function that we are mocking
                # + this way we can force the function rase an error
                call_command('wait_for_db')
                self.assertEqual(gi.call_count, 6)
  ```

## User App

[Go Back to Contents](#contents)

- Now we are going to create a **user** app
- This app will allow us to CRUD our user's endpoints
- On `Terminal`

  ```Bash
    docker-compose run --rm app sh -c "python manage.py startapp user"
  ```

### User - Folder and Files

[Go Back to Contents](#contents)

- After creating the user's app we are going to delete some files and create some files

  ```Bash
    .
    ├── migrations          <--- Delete
    │   └── __init__.py     <--- Delete
    ├── __init__.py
    ├── admin.py            <--- Delete
    ├── apps.py
    ├── models.py           <--- Delete
    ├── tests.py            <--- Delete
    └── views.py
  ```

  - we are deleting the migration, admin.py, models.py, because we are using our **core** app for that, so we don't need them here
  - we are deleting the tests.py, because we need a folder for our tests

  ```Bash
    touch app/user/tests/__init__.py + test_user_api.py app/user/urls.py + serializers.py
  ```

### User - Register New App

[Go Back to Contents](#contents)

- in `app/config/settings.py`

  - Add our new **user** app
  - Install **rest_framework.authtoken** to create auth token

    ```Python
      INSTALLED_APPS = [
          'core',
          'user',
          'rest_framework',
          'rest_framework.authtoken',
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',
      ]
    ```

### User - Serializers

[Go Back to Contents](#contents)

- in `app/user/serializers.py`

  - Import our model (`get_user_model`)
  - Import **serializers** from `rest_framework`
  - Create a sub-class named **Meta**
    - Responsible for serializing the incoming/exporting data as JSON
    - We need to add **model** and **fields** - **(required)**
    - extra_kwargs if we want to add extra config to a certain field
  - Override the **create()** to use our custom `create_user`

  ```Python
    from django.contrib.auth import get_user_model
    # import user model
    # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.get_user_model
    from rest_framework import serializers
    # https://www.django-rest-framework.org/api-guide/serializers/#modelserializer


    class UserSerializer(serializers.ModelSerializer):
        # + To create a new serializer we need to inherit
        # + from serializers.ModelSerializer
        # - Basically a serializer is a parser that converts
        # - Incoming data or exporting/sending data as JSON
        """Serializer for the user object"""
        class Meta:
            model = get_user_model()
            # ! 1) we need to define the model
            fields = ('email', 'password', 'name')
            # ! 2) these are the fields that we want to include
            # ! in our serializer to be converted to/from JSON
            # ! these are the fields available to read/write
            extra_kwargs = {
                'password': {
                    'write_only': True,
                    'min_length': 5
                }
            }
            # ! 3) extra_kwargs, allows us to configure extra
            # ! settings in our ModelSerializer
            # + In this case we are ensuring that our password is
            # + write_only (we connot read the password) and the
            # + min_length is 5 characters

        # ! We now need to overwrite the create function
        def create(self, validate_data):
            # https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
            """Create a new user with encrypted password and return it"""
            # + In this case we are using our custom create_user from our
            # + UserManager to create a new user and hash de password
            # - The validate_data is our fields that we specified in our
            # - Meta class
            # ? The create() method, receives the validate_data as second arg
            return get_user_model().objects.create_user(**validate_data)
  ```

### User - View (Controllers)

[Go Back to Contents](#contents)

- in `app/user/views.py`

  - Create our view to create users

    ```Python
      from rest_framework import generics
      # Import the generics we need the CreateAPIView to create our API
      from user.serializers import UserSerializer
      # Import the user serializer


      class CreateUserView(generics.CreateAPIView):
          """Create a new user in the system"""
          serializer_class = UserSerializer
          # ! all we need to specify in our class is the serializer_class
          # ! and point to the our Serializer
    ```

### User - Urls (Routes)

[Go Back to Contents](#contents)

- in `app/user/urls.py`

  ```Python
    from django.urls import path
    # Import path to build our routes
    from user import views
    # import the the user views from user

    app_name = 'user'
    # The app_name is necessary to help use identify where the request is coming
    # from when we use the reverse method to get the url

    urlspatterns = [
        path('create/', views.CreateUserView.as_view(), name='create'),
    ]
  ```

### User - Register Base API Url

[Go Back to Contents](#contents)

- in `app/config/urls.py`

  - Import **include**
  - Add a new route to the user's app

    ```Python
      from django.contrib import admin
      from django.urls import path, include
      from django.conf.urls.static import static
      from django.conf import settings

      urlpatterns = [
          path('admin/', admin.site.urls),
          path('api/user/', include('user.urls'))
      ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

### User - Token Authentication

[Go Back to Contents](#contents)

- in `app/user/serializers.py`

  - We are going to create a new serializer to handle auth token

    ```Python
      from django.contrib.auth import get_user_model, authenticate
      # django comes authenticate funcion, it's a helper function to allow use
      # easily authenticate a user by providing the username and password
      from django.utils.translation import ugettext_lazy as _
      # Import the translation module
      from rest_framework import serializers


      class UserSerializer(serializers.ModelSerializer):
          """Serializer for the user object"""
          class Meta:
              model = get_user_model()
              fields = ('email', 'password', 'name')
              extra_kwargs = {
                  'password': {
                      'write_only': True,
                      'min_length': 5
                  }
              }

          def create(self, validate_data):
              """Create a new user with encrypted password and return it"""
              return get_user_model().objects.create_user(**validate_data)


      class AuthTokenSerializer(serializers.Serializer):
          # we inherit the auth token from serializers.Serializer
          """Serializer for the user authenticate object"""
          # + Create our serializer fields
          email = serializers.CharField()
          password = serializers.CharField(
              style={'input_type': 'password'},
              trim_whitespace=False
          )

          # ! Create our validate function that receives the attributes
          # ! from our serializer in this case email and password will be
          # ! parsed as attrs
          def validate(self, attrs):
              """Validate and authenticate the user"""
              # + attrs.get is how we get the attribute
              email = attrs.get('email')
              password = attrs.get('password')
              user = authenticate(
                  request=self.context.get('request'),
                  username=email,
                  password=password
              )
              # + 1st argument is the request that we want to authenticate
              # - self.context.get('request') we can have access to the request
              # - that was made
              # + 2nd argument is the username
              # + 3rd argument is the password

              if not user:
                  # + if not enable to authenticate raise a ValidationError
                  msg = _('Unable to authenticate with provided credentials.')
                  raise serializers.ValidationError(msg, code='authentication')

              # + if success, add a user field to attrs and return the attrs
              attrs['user'] = user
              # + we always return the attrs object
              return attrs
    ```

- in `app/user/views.py`

  - **ObtainAuthToken**

    - When using **[TokenAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#by-exposing-an-api-endpoint)**, you may want to provide a mechanism for clients to obtain a token given the username and password. REST framework provides a built-in view to provide this behavior. To use it, add the obtain_auth_token view to your URLconf:

      ```Python
        from rest_framework.authtoken import views
        urlpatterns += [
            path('api-token-auth/', views.obtain_auth_token)
        ]
      ```

    - The `obtain_auth_token` view will return a **JSON** response when valid `username` and `password` fields are POSTed to the view using form data or JSON:

      ```Python
        { 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
      ```

    - If you need a customized version of the `obtain_auth_token` view, you can do so by subclassing the **ObtainAuthToken** view class, and using that in your url conf instead.
    - For example, you may return additional user information beyond the **token** value:

      ```Python
        from rest_framework.authtoken.views import ObtainAuthToken
        from rest_framework.authtoken.models import Token
        from rest_framework.response import Response

        class CustomAuthToken(ObtainAuthToken):

            def post(self, request, *args, **kwargs):
                serializer = self.serializer_class(data=request.data,
                                                  context={'request': request})
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })
      ```

      - And in your `urls.py`:

        ```Python
          urlpatterns += [
              path('api-token-auth/', CustomAuthToken.as_view())
          ]
        ```

  - **api_settings**

    - If you need to access the values of REST framework's API settings in your project, you should use the **api_settings** object. For example.

      ```Python
        from rest_framework.settings import api_settings

        print(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
      ```

    - The **api_settings** object will check for any user-defined settings, and otherwise fall back to the default values. Any setting that uses string import paths to refer to a class will automatically import and return the referenced class, instead of the string literal.

  ```Python
    from rest_framework import generics
    from user.serializers import UserSerializer, AuthTokenSerializer
    from rest_framework.authtoken.views import ObtainAuthToken
    # Import ObtainAuthToken
    from rest_framework.settings import api_settings
    # Import api_settings


    class CreateUserView(generics.CreateAPIView):
        """Create a new user in the system"""
        serializer_class = UserSerializer


    class CreateTokenView(ObtainAuthToken):
        """Create a new token for user"""
        serializer_class = AuthTokenSerializer
        renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
        # + If you need to access the values of REST framework's API settings in
        # +     your project, you should use the api_settings object. For example.
        # + The api_settings object will check for any user-defined settings, and
        # +     otherwise fall back to the default values. Any setting that uses
        # +     string import paths to refer to a class will automatically import
        # +     and return the referenced class, instead of the string literal.
  ```

- in `app/user/urls.py`

  - Add a new route to handle token

    ```Python
      from django.urls import path
      from user import views

      app_name = 'user'

      urlpatterns = [
          path('create/', views.CreateUserView.as_view(), name='create'),
          path('token/', views.CreateTokenView.as_view(), name='token'),
      ]
    ```

- On `broswer`

  - if we naviagte to [http://localhost:8000/api/user/](http://localhost:8000/api/user/)

    - We will see that we have 2 routes available

      ![](https://i.imgur.com/QkgnTy6.png)

    - [http://localhost:8000/api/user/create/](http://localhost:8000/api/user/create/)

      ![](https://i.imgur.com/3b8mgRS.png)

      - Create a new user

        ![](https://i.imgur.com/O4FCLHW.png)
        ![](https://i.imgur.com/GrzAnSc.png)

    - [http://localhost:8000/api/user/token/](http://localhost:8000/api/user/token/)

      - Atuthenticate the user

        ![](https://i.imgur.com/rmxhyn4.png)

### User - Manage Endpoints

[Go Back to Contents](#contents)

- in `app/user/views.py`

  - Create our **ManageUserView** to manage our logged in users endpoints
  - Import **authentication** and **permissions** from `rest_framework`
    - we are going to use with our user endpoints

  ```Python
    from rest_framework import generics, authentication, permissions
    # import authentication and permissions, we are going to use with our
    # user endpoints
    from user.serializers import UserSerializer, AuthTokenSerializer
    from rest_framework.authtoken.views import ObtainAuthToken
    from rest_framework.settings import api_settings


    class CreateUserView(generics.CreateAPIView):
        """Create a new user in the system"""
        serializer_class = UserSerializer


    class CreateTokenView(ObtainAuthToken):
        """Create a new token for user"""
        serializer_class = AuthTokenSerializer
        renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


    # ! Create our manage user view and
    # ! we inherits from generics.RetrieveUpdateAPIView
    class ManageUserView(generics.RetrieveUpdateAPIView):
        """Manage the authenticate user"""
        serializer_class = UserSerializer
        authentication_classes = (authentication.TokenAuthentication,)
        # + authentication_classes is the mechanism that authenticate the user
        # + in this case we are using TokenAuthentication, but could it be
        # + cookie authentication, and so on..
        permission_classes = (permissions.IsAuthenticated,)
        # + permission_classes is the lvl of permission that the user has
        # + in this case we are only requiring the user be authenticated to
        # + use this API

        # + We are going to override the get_object to retrieve the model
        # + for logged in user, in other words, it will return the user that
        # + is authenticated
        def get_object(self):
            """Retreive and return authenticate user"""
            return self.request.user
            # + Because of the permission_classes the request will have the
            # + Authenticated user in it
  ```

- in `app/user/serializers.py`

  - We need to override the **update** function to handle our update

    ```Python
      from django.contrib.auth import get_user_model, authenticate
      from django.utils.translation import ugettext_lazy as _
      from rest_framework import serializers


      class UserSerializer(serializers.ModelSerializer):
          """Serializer for the user object"""
          class Meta:
              ...

          def create(self, validate_data):
              ...

          # + With update() is similar to get(), with update() we need
          # + to pass the instance and validate_data
          # - the instance will be the model linked to our user (get_user_mode())
          # - the validate_data will be our incoming form (fields)
          def update(self, instance, validate_data):
              """Update a user, setting the password correctly and return it"""
              password = validate_data.pop('password', None)
              # + first we remove the password from the form
              # - with .pop() function, we need to provide a default value
              user = super().update(instance, validate_data)
              # + with the rest of of the form we update the instance with
              # + validate_data
              # - The super() will call ModelSerializer the default udpate function

              if password:
                  user.set_password(password)
              user.save()

              return user


      class AuthTokenSerializer(serializers.Serializer):
          ...
    ```

- in `app/user/urls.py`

  - Update our route to handel put/patch update

    ```Python
      from django.urls import path
      from user import views

      app_name = 'user'

      urlpatterns = [
          path('create/', views.CreateUserView.as_view(), name='create'),
          path('token/', views.CreateTokenView.as_view(), name='token'),
          path('me/', views.ManageUserView.as_view(), name='me')
      ]
    ```

### User - Tests

[Go Back to Contents](#contents)

- in `app/user/tests/test_user_api.py`

  ```Python
    from django.test import TestCase
    # import our test case
    from django.contrib.auth import get_user_model
    # import our user model
    from django.urls import reverse
    # import reverse to generate our api urls

    # ! Import rest_framework helper test tools
    from rest_framework.test import APIClient
    # import APIClient responsible for making requests to our APIs and check what is the response
    from rest_framework import status
    # import status just to convert the status code in a more readable form

    # ! Get the user url
    CREATE_USER_URL = reverse('user:create')
    TOKEN_URL = reverse('user:token')
    ME_URL = reverse('user:me')


    def create_user_db(**params):
        # + Helper function to create multiple users for our tests
        return get_user_model().objects.create_user(**params)


    class PublicUserApiTests(TestCase):
        """Test the users API (public)"""

        def setUp(self):
            # create a variable (client)
            # assign the APIClient() function to make http requests
            self.client = APIClient()

        def test_create_valid_user_success(self):
            """Test creating user with valid payload is successful"""
            payload = {
                'email': 'test@test.com',
                'password': 'test123',
                'name': 'Test Name'
            }
            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            user = get_user_model().objects.get(**res.data)
            self.assertTrue(user.check_password(payload['password']))
            self.assertNotIn('password', res.data)

        def test_user_exists(self):
            """Test creating user that already exists fails"""
            payload = {
                'email': 'test@test.com',
                'password': 'test123',
                'name': 'Test Name'
            }
            create_user_db(**payload)
            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_password_too_short(self):
            """The password must be more than 5 characters"""
            payload = {
                'email': 'test@test.com',
                'password': '123',
                'name': 'Test Name'
            }
            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(
                email=payload['email']).exists()
            self.assertFalse((user_exists))

        def test_create_token_for_user(self):
            """Test that a token is created for the user"""
            payload = {
                'email': 'test@test.com',
                'password': 'test123'
            }
            create_user_db(**payload)
            res = self.client.post(TOKEN_URL, payload)
            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        def test_create_token_invalid_credentials(self):
            """Test that token is not created if invalid credentials are given"""
            payload = {
                'email': 'test@test.com',
                'password': 'test123'
            }
            create_user_db(**payload)
            wrong_payload = {
                'email': 'test@test.com',
                'password': 'wrong_password'
            }
            res = self.client.post(TOKEN_URL, wrong_payload)
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_no_user(self):
            """Test that token is not created if user doesn't exist"""
            bad_payload = {
                'email': 'no_user@test.com',
                'password': 'test123'
            }
            res = self.client.post(TOKEN_URL, bad_payload)
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_missing_field(self):
            """Test that email and password are required"""
            res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_retrive_user_unauthorized(self):
                """Test that authentication is required for users"""
                res = self.client.get(ME_URL)
                self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    class PrivateUserApiTests(TestCase):
        """Test API requests that require authentication"""

        def setUp(self):
            payload = {
                "email": "authenticated@test.com",
                "password": "test123",
                "name": "Roger Authenticated"
            }
            self.user = create_user_db(**payload)
            self.client = APIClient()
            self.client.force_authenticate(user=self.user)
            # + uses the client helper function (force_authenticate) to
            # + authenticate the users
            # - in other words, all requests that we do with this user
            # - will be authenticated

        def test_retrive_profile_success(self):
            """Test retrieving profile for logged in used"""
            res = self.client.get(ME_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, {
                'name': self.user.name,
                'email': self.user.email
            })

        def test_post_profile_not_allowed(self):
            """Test that POST is not allowed on the me url"""
            res = self.client.post(ME_URL, {})
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_update_user_profile(self):
            """Test updating the user profile for authenticated user"""
            payload = {
                "name": "Roger Updated",
                "password": "newpassword123"
            }
            res = self.client.patch(ME_URL, payload)
            self.user.refresh_from_db()
            # + helper function to refresh the database with the latest update
            self.assertEqual(self.user.name, payload["name"])
            self.assertTrue(self.user.check_password(payload["password"]))
            self.assertEqual(res.status_code, status.HTTP_200_OK)
  ```

## Recipe APP

### Recipe - Create New App

[Go Back to Contents](#contents)

- On `Terminal`

  ```Bash
    docker-compose run --rm app sh -c "python manage.py start recipe"
  ```

### Recipe - Folder and Files

[Go Back to Contents](#contents)

- Create folder and files, and remove files

  ```Bash
    touch app/recipe/serializer.py + urls.py + tests/__init__.py + test_tags_api.py
  ```

- Delete `migrations folder`, `admin.py`, `models.py`, and `test.py`

  ```Bash
    .
    ├── test
    │   ├── __init__.py
    │   └── test_tags_api.py
    ├── __init__.py
    ├── apps.py
    ├── serializers.py
    └── views.py
  ```

### Recipe - Register a New App

[Go Back to Contents](#contents)

- in `app/config/settings.py`

  ```Bash
    INSTALLED_APPS = [
        'core',
        'user',
        'recipe',
        'rest_framework',
        'rest_framework.authtoken',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
  ```

### Recipe - Register Base API Url

[Go Back to Contents](#contents)

- in `app/config/urls.py`

  ```Python
    from django.contrib import admin
    from django.urls import path, include
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/user/', include('user.urls')),
        path('api/recipe/', include('recipe.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

### Tag

#### Tag - Models

[Go Back to Contents](#contents)

- in `app/core/models.py`

  - Import **settings** from `django.conf`

    - [ForeignKey.swappable](https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.swappable)

      - Controls the migration framework’s reaction if this ForeignKey is pointing at a swappable model. If it is `True` - the default - then if the ForeignKey is pointing at a model which matches the current value of **settings.AUTH_USER_MODEL** (or another swappable model setting) the relationship will be stored in the migration using a reference to the setting, not to the model directly.

      - You only want to override this to be `False` if you are sure your model should always point towards the swapped-in model - for example, if it is a profile model designed specifically for your custom user model.

  - Create a new **Tag** class

    - [Model instance methods](https://docs.djangoproject.com/en/3.1/ref/models/instances/#other-model-instance-methods)
    - \***\*str**()** - The `__str__()` method is called whenever you call **str()** on an object. Django uses **str(obj)\*\* in a number of places. Most notably, to display an object in the Django admin site and as the value inserted into a template when it displays an object. Thus, you should always return a nice, human-readable representation of the model from the `__str__()` method.

    ```Python
      from django.conf import settings
      # Import settings, best practice to retrive the AUTH_USER_MODEL
      # We could acess directly
      # This is the recomended way to retrive different settings from
      # the settings.py

      ...

      class Tag(models.Model):
      """Tag to be used for a recipe"""
      name = models.CharField(max_length=255)
      user = models.ForeignKey(
          settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE
      )

      def __str__(self):
          return self.name
    ```

#### Tag - Migrations

[Go Back to Contents](#contents)

- On `Terminal`

  - After updating the models, make migrations to apply the modifications

    ```Bash
      docker-compose run --rm app sh -c "python manage.py makemigrations"
      docker-compose run --rm app sh -c "python manage.py migrate"
    ```

#### Tag - Register App Admin Panel

[Go Back to Contents](#contents)

- in `app/core/admin.py`

  ```Python
    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    from django.utils.translation import gettext as _
    from core import models


    class UserAdmin(BaseUserAdmin):
        ...


    admin.site.register(models.User, UserAdmin)
    admin.site.register(models.Tag)
  ```

#### Tag - Serializer

[Go Back to Contents](#contents)

- in `app/recipe/serializers.py`

  - The [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) class provides a shortcut that lets you automatically create a `Serializer` class with fields that correspond to the Model fields.
  - The **ModelSerializer** class is the same as a regular **Serializer** class, except that:

    - It will automatically generate a set of fields for you, based on the model.
    - It will automatically generate validators for the serializer, such as unique_together validators.
    - It includes simple default implementations of `.create()` and `.update()`.

  ```Python
    from rest_framework import serializers
    from core.models import Tag


    class TagSerializer(serializers.ModelSerializer):
        """Serializer for tag objects"""
        class Meta:
            model = Tag
            fields = ('id', 'name')
            read_only_fields = ('id',)
  ```

#### Tag - Views

[Go Back to Contents](#contents)

- in `app/recipe/views.py`

  - **[ViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#viewset)**

    - The `ViewSet` class inherits from `APIView`. You can use any of the standard attributes such as `permission_classes`, `authentication_classes` in order to control the API policy on the viewset.
    - The `ViewSet` class does not provide any implementations of actions. In order to use a `ViewSet` class you'll override the class and define the action implementations explicitly.
    - **[GenericViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#genericviewset)**

      - The `GenericViewSet` class inherits from `GenericAPIView`, and provides the default set of `get_object`, `get_queryset` methods and other generic view base behavior, but does not include any actions by default.
      - In order to use a `GenericViewSet` class you'll override the class and either mixin the required mixin classes, or define the action implementations explicitly.

    - **[ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)**
      - The `ModelViewSet` class inherits from `GenericAPIView` and includes implementations for various actions, by mixing in the behavior of the various mixin classes.
      - The actions provided by the `ModelViewSet` class are `.list()`, `.retrieve()`, `.create()`, `.update()`, `.partial_update()`, and `.destroy()`.

  - **[Mixins](https://www.django-rest-framework.org/api-guide/generic-views/#mixins)**

    - The mixin classes provide the actions that are used to provide the basic view behavior. Note that the mixin classes provide action methods rather than defining the handler methods, such as .`get()` and `.post()`, directly. This allows for more flexible composition of behavior.
    - **ListModelMixin**
      - Provides a `.list(request, *args, **kwargs)` method, that implements listing a queryset.
      - If the queryset is populated, this returns a `200 OK` response, with a serialized representation of the queryset as the body of the response. The response data may optionally be paginated.

  - **[Custom ViewSet base classes](https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes)**

    - You may need to provide custom `ViewSet` classes that do not have the full set of `ModelViewSet` actions, or that customize the behavior in some other way.
    - Example:

      - To create a base viewset class that provides **create**, **list** and **retrieve** operations, inherit from `GenericViewSet`, and mixin the required actions:

        ```Python
          from rest_framework import mixins

          class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                          mixins.ListModelMixin,
                                          mixins.RetrieveModelMixin,
                                          viewsets.GenericViewSet):
              """
              A viewset that provides `retrieve`, `create`, and `list` actions.

              To use it, override the class and set the `.queryset` and
              `.serializer_class` attributes.
              """
              pass
        ```

  ```Python
    from rest_framework import viewsets, mixins
    # Import GenericViewSet and Mixins
    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAuthenticated
    from core.models import Tag
    from recipe import serializers


    class TagViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
        # + ListModelMixin adds the option to list the items
        # + CreateModelMixing adds the option to create  an item
        """Manage tags in the database"""
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)
        queryset = Tag.objects.all()
        serializer_class = serializers.TagSerializer

        # + Overrite the get_queryset - ListModelMixins
        def get_queryset(self):
            """Return objects for the current authenticated user only"""
            return self.queryset.filter(user=self.request.user).order_by('-name')
            # referencing the queryset above

        # + Overrite the perform_create - ListModelMixins
        def perform_create(self, serializer):
            """Create a new tag"""
            serializer.save(user=self.request.user)
            # - we set the user to the authenticated user
            # - use the serializer to format properly and save
  ```

#### Tag - Urls (Router)

[Go Back to Contents](#contents)

- in `app/recipe/urls.py`

  ```Python
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from recipe import views

    app_name = 'recipe'

    router = DefaultRouter()
    router.register('tags', views.TagViewSet)

    urlpatterns = [
        path('', include(router.urls))
    ]
  ```

#### Tag - Test Model

[Go Back to Contents](#contents)

- in `app/core/tests/test_models.py`

  - Add a new test to check the string representattion of the **Tag Model**

    ```Python
      def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )
        self.assertEqual(str(tag), tag.name)
    ```

#### Tag - Tests

[Go Back to Contents](#contents)

- in `app/recipe/test/test_tags_api.py`

  ```Python
    from django.contrib.auth import get_user_model
    from django.test import TestCase
    from django.urls import reverse
    from rest_framework import status
    from rest_framework.test import APIClient
    from core.models import Tag
    from recipe.serializers import TagSerializer

    TAGS_URL = reverse('recipe:tag-list')


    class PublicTagsApiTests(TestCase):
        """Test the public available tags API"""

        def setUp(self):
            self.client = APIClient()

        def test_login_required(self):
            """Test that login is required for retrieving tags"""
            res = self.client.get(TAGS_URL)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    class PrivateTagsApiTests(TestCase):
        """Test the authorized user tags API"""

        def setUp(self):
            self.user = get_user_model().objects.create_user(
                'test@test.com',
                'password123'
            )
            self.client = APIClient()
            self.client.force_authenticate(self.user)

        def test_retrive_tags(self):
            """Test retrieving tags"""
            Tag.objects.create(user=self.user, name="Vegan")
            Tag.objects.create(user=self.user, name="Dessert")
            res = self.client.get(TAGS_URL)
            tags = Tag.objects.all().order_by('-name')
            serializer = TagSerializer(tags, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_tags_limited_to_user(self):
            """Test that tags returned are for the authenticated user"""
            user2 = get_user_model().objects.create_user(
                'test2@test.com',
                'password123'
            )
            Tag.objects.create(user=user2, name='Fruity')
            tag = Tag.objects.create(user=self.user, name='Comfort Food')

            res = self.client.get(TAGS_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.data[0]['name'], tag.name)

        def test_create_tag_successful(self):
            """Test creating a new tag"""
            payload = {
                "name": "Test Tag"
            }
            res = self.client.post(TAGS_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            exists = Tag.objects.filter(
                user=self.user,
                name=payload['name']
            ).exists()
            self.assertTrue(exists)

        def test_create_tag_invalid(self):
            """Test creating a new tag with invalid payload"""
            payload = {
                "name": ""
            }
            res = self.client.post(TAGS_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  ```

### Ingredient

#### Ingredient - Folder and Files

[Go Back to Contents](#contents)

- Create the following file

  ```Bash
    touch app/recipe/tests/test_ingredients_api.py
  ```

#### Ingredient - Models

[Go Back to Contents](#contents)

- in `app/core/models.py`

  - Update the core model, add a new calss called **Ingredient**

    ```Python
      class Ingredient(models.Model):
        """Ingredient to be used in a recipe"""
        name = models.CharField(max_length=255)
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
        )

        def __str__(self):
            return self.name
    ```

#### Ingredient - Migrations

[Go Back to Contents](#contents)

- On `Terminal`

  - After updating the models, make migrations to apply the modifications

    ```Bash
      docker-compose run --rm app sh -c "python manage.py makemigrations"
      docker-compose run --rm app sh -c "python manage.py migrate"
    ```

#### Ingredient - Register App Admin Panel

[Go Back to Contents](#contents)

- in `app/core/admin.py`

  ```Python
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    from django.utils.translation import gettext as _
    from core import models


    class UserAdmin(BaseUserAdmin):
        ...


    admin.site.register(models.User, UserAdmin)
    admin.site.register(models.Tag)
    admin.site.register(models.Ingredient)
  ```

#### Ingredient - Serializer

[Go Back to Contents](#contents)

- in `app/recipe/serializers.py`

  - Import our Ingredient model
  - Add a new serializer

    ```Python
      from rest_framework import serializers
      from core.models import Tag, Ingredient


      class TagSerializer(serializers.ModelSerializer):
          """Serializer for tag objects"""
          class Meta:
              model = Tag
              fields = ('id', 'name')
              read_only_fields = ('id',)


      class IngredientSerializer(serializers.ModelSerializer):
          """Serializer for ingredients objects"""
          class Meta:
              model = Ingredient
              fields = ('id', 'name')
              read_only_fields = ('id',)
    ```

#### Ingredient - Views

[Go Back to Contents](#contents)

- in `app/recipe/views.py`

  - Import our Ingredient model
  - Create a new ViewSet

    ```Python
      from rest_framework import viewsets, mixins
      from rest_framework.authentication import TokenAuthentication
      from rest_framework.permissions import IsAuthenticated
      from core.models import Tag, Ingredient
      from recipe import serializers


      class TagViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
          ...


      class IngredientViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
          """Manage ingredients in the database"""
          authentication_classes = (TokenAuthentication,)
          permission_classes = (IsAuthenticated,)
          queryset = Ingredient.objects.all()
          serializer_class = serializers.IngredientSerializer

          def get_queryset(self):
              """Returns object for the current authenticated user only"""
              return self.queryset.filter(user=self.request.user).order_by("-name")

          def perform_create(self, serializers):
              """Create a new ingredient"""
              serializers.save(user=self.request.user)
    ```

#### Ingredient - Urls (Router)

[Go Back to Contents](#contents)

- in `app/recipe/urls.py`

  - Add a new ViewSet router

    ```Python
      from django.urls import path, include
      from rest_framework.routers import DefaultRouter
      from recipe import views

      app_name = 'recipe'

      router = DefaultRouter()
      router.register('tags', views.TagViewSet)
      router.register('ingredients', views.IngredientViewSet)

      urlpatterns = [
          path('', include(router.urls))
      ]
    ```

#### Ingredient - Test Models

[Go Back to Contents](#contents)

- in `app/core/tests/test_models.py`

  - Add a new test to check the string representation of the **Ingredient Model**

    ```Python
      def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)
    ```

#### Ingredient - Test

[Go Back to Contents](#contents)

- in `app/recipe/tests/test_ingredients_api.py`

  ```Python
    from django.contrib.auth import get_user_model
    from django.urls import reverse
    from django.test import TestCase
    from rest_framework import status
    from rest_framework.test import APIClient
    from core.models import Ingredient
    from recipe.serializers import IngredientSerializer

    INGREDIENTS_URL = reverse('recipe:ingredient-list')


    class PublicIngredientsApiTests(TestCase):
        """Test the public available ingredients API"""

        def setUp(self):
            self.client = APIClient()

        def test_login_required(self):
            """Test that login is required to access the endpoing"""
            res = self.client.get(INGREDIENTS_URL)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    class PrivateIngredientsApiTests(TestCase):
        """Test the private ingredients API"""

        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                'test@test.com',
                'password123'
            )
            self.client.force_authenticate(self.user)

        def test_retrieve_ingredients_list(self):
            """Test retriving a list of ingredients"""
            Ingredient.objects.create(user=self.user, name="Kale")
            Ingredient.objects.create(user=self.user, name="Salt")
            res = self.client.get(INGREDIENTS_URL)
            ingredients = Ingredient.objects.all().order_by("-name")
            serializer = IngredientSerializer(ingredients, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_ingredients_limited_to_user(self):
            """Test that ingredients for the authenticated user are returned"""
            user2 = get_user_model().objects.create_user(
                "user2@test.com",
                "password123"
            )
            Ingredient.objects.create(user=user2, name="Vinegar")
            ingredient = Ingredient.objects.create(user=self.user, name="Tumeric")
            res = self.client.get(INGREDIENTS_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.data[0]['name'], ingredient.name)

        def test_create_ingredient_successful(self):
            """Test create a new ingredient"""
            payload = {
                "name": "Cabbage"
            }
            res = self.client.post(INGREDIENTS_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            exists = Ingredient.objects.filter(
                user=self.user,
                name=payload['name']
            ).exists()
            self.assertTrue(exists)

        def test_create_ingredient_invalid(self):
            """Test creating invalid ingredient fails"""
            payload = {
                "name": ""
            }
            res = self.client.post(INGREDIENTS_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  ```

### Recipe - REFACTOR View (Controller)

[Go Back to Contents](#contents)

- in `app/recipe/views.py`

  - Let's refactor our ViewSets to dry the code
  - We can create our **BaseRecipeViewSet**

    ```Python
      from rest_framework import viewsets, mixins
      from rest_framework.authentication import TokenAuthentication
      from rest_framework.permissions import IsAuthenticated
      from core.models import Tag, Ingredient
      from recipe import serializers


      class BaseRecipeViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
          """Base ViewSet for user owned recipe attributes"""
          authentication_classes = (TokenAuthentication,)
          permission_classes = (IsAuthenticated,)

          def get_queryset(self):
              """Return object for the authenticated user only"""
              return self.queryset.filter(user=self.request.user).order_by("-name")

          def perform_create(self, serializer):
              """Create a new object"""
              serializer.save(user=self.request.user)


      class TagViewSet(BaseRecipeViewSet):
          """Manage tags in the database"""
          queryset = Tag.objects.all()
          serializer_class = serializers.TagSerializer


      class IngredientViewSet(BaseRecipeViewSet):
          """Manage ingredients in the database"""
          queryset = Ingredient.objects.all()
          serializer_class = serializers.IngredientSerializer
    ```

### Recipe

#### Recipe - Folder and Files

[Go Back to Contents](#contents)

- Create a new test case

  ```Bash
    touch app/recipe/tests/test_recipe_api.py
  ```

#### Recipe - Model

[Go Back to Contents](#contents)

- in `app/core/models.py`

  - Add a Recipe Model

    - [ManyToManyField](https://docs.djangoproject.com/en/3.1/ref/models/fields/#manytomanyfield)
      - we pass the argument as string, this way we don't need to worry about the order of the classes. Otherwise, we need to declare first `ngredient` and `Tag` before the `Recipe` class
    - `blank=True` this means that this field is optional and the default value is an empty string. If we set to `null` we have to check if is `not null` and if is `not empty string`

    ```Python
      class Recipe(models.Model):
        """Recipe object"""
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
        )
        title = models.CharField(max_length=255)
        time_minutes = models.IntegerField()
        price = models.DecimalField(max_digits=5, decimal_places=2)
        link = models.CharField(max_length=255, blank=True)
        ingredients = models.ManyToManyField('Ingredient')
        tags = models.ManyToManyField('Tag')

        def __str__(self):
            return self.title
    ```

#### Recipe - Migrations

[Go Back to Contents](#contents)

- On `Terminal`

  - After updating the models, make migrations to apply the modifications

    ```Bash
      docker-compose run --rm app sh -c "python manage.py makemigrations"
      docker-compose run --rm app sh -c "python manage.py migrate"
    ```

#### Recipe - Register App Admin Panel

[Go Back to Contents](#contents)

- in `app/core/admin.py`

  ```Python
    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    from django.utils.translation import gettext as _
    from core import models


    class UserAdmin(BaseUserAdmin):
        ...


    admin.site.register(models.User, UserAdmin)
    admin.site.register(models.Tag)
    admin.site.register(models.Ingredient)
    admin.site.register(models.Recipe)
  ```

#### Recipe - Serializer

[Go Back to Contents](#contents)

- in `app/recipe/serializers.py`

  - Import Recipe model
  - We are going to create the **RecipeSerializer**
  - With **Recipe** model we have some **ManyToMany** RelatedFields and we need to get the ids to those references
  - [https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield](https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield)

    ```Python
      from rest_framework import serializers
      from core.models import Tag, Ingredient, Recipe


      class TagSerializer(serializers.ModelSerializer):
          """Serializer for tag objects"""
          class Meta:
              model = Tag
              fields = ('id', 'name')
              read_only_fields = ('id',)


      class IngredientSerializer(serializers.ModelSerializer):
          """Serializer for ingredients objects"""
          class Meta:
              model = Ingredient
              fields = ('id', 'name')
              read_only_fields = ('id',)


      class RecipeSerializer(serializers.ModelSerializer):
          """Serializer for recipe objects"""
          # = References - Getting IDs
          ingredients = serializers.PrimaryKeyRelatedField(
              many=True, queryset=Ingredient.objects.all()
          )
          # https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
          # many equals True, because this is a many to many field
          #    allow many
          # queryset to list all ingredients
          #    this will list only the Ids
          # to retrive the full object, we will create a detail API for that
          tags = serializers.PrimaryKeyRelatedField(
              many=True, queryset=Tag.objects.all()
          )

          class Meta:
              model = Recipe
              fields = ('id', 'title', 'ingredients', 'tags',
                        'time_minutes', 'price', 'link')
              read_only_fields = ('id',)
              # ! Good practice to prevent the user from updating the ID
    ```

#### Recipe - Views (Controllers)

[Go Back to Contents](#contents)

- in `app/recipe/views.py`

  - Import our **Recipe** model
  - Crate a new viewset, we are going to inherite from `viewsets.ModelsViewSet` bacuse we need all the functionaties to CRUD this model
  - then we override the `get_queryset()` to only return objects from the authenticated user
  - Override the **get_serializer_class** to handle different types of requests

    - Get all recipes
    - Get one recipe
      - With this option, the user will received the whole recipe with ManyToMany fields populated with their information
    - Override the **perform_create** to use the authenticated user to create a new recipe

    ```Python
      from rest_framework import viewsets, mixins
      from rest_framework.authentication import TokenAuthentication
      from rest_framework.permissions import IsAuthenticated
      from core.models import Tag, Ingredient, Recipe
      from recipe import serializers


      class BaseRecipeViewSet(viewsets.GenericViewSet,
          ...


      class TagViewSet(BaseRecipeViewSet):
          ...


      class IngredientViewSet(BaseRecipeViewSet):
          ...


      class RecipeViewSet(viewsets.ModelViewSet):
          """Manage recipes in the database"""
          serializer_class = serializers.RecipeSerializer
          queryset = Recipe.objects.all()
          authentication_classes = (TokenAuthentication,)
          permission_classes = (IsAuthenticated,)

          def get_queryset(self):
              """Retrieve the recipes for the authenticated user"""
              return self.queryset.filter(user=self.request.user)

          def get_serializer_class(self):
              # + override the get_serializer_class to handle different
              # + requests (get 1 item or get all items)
              # + # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
              """Return appropriate serializer class"""
              if self.action == 'retrieve':
                  # + we user self.action to check the type of the request
                  # + 'retrieve' means 1 recipe
                  return serializers.RecipeDetailSerializer
              return self.serializer_class(self):

          def perform_create(self, serializer):
              # + override the create funtion to use our authenticated user
              # + to create new recipes
              """Create a new recipe"""
              serializer.save(user=self.request.user)
    ```

#### Recipe - Urls (Router)

[Go Back to Contents](#contents)

- in `app/recipe/urls.py`

  - Register a the `recipes` urls

    ```Python
      from django.urls import path, include
      from rest_framework.routers import DefaultRouter
      from recipe import views

      app_name = 'recipe'

      router = DefaultRouter()
      router.register('tags', views.TagViewSet)
      router.register('ingredients', views.IngredientViewSet),
      router.register('recipes', views.RecipeViewSet),


      urlpatterns = [
          path('', include(router.urls))
      ]
    ```

#### Recipe - Test Models

[Go Back to Contents](#contents)

- in `app/core/tests/test_models.py`

  - Add a new test to check the string representation of the **Recipe Model**

    ```Python
      def test_recipe_str(self):
          """Test the recipe string representation"""
          recipe = models.Recipe.objects.create(
              user=sample_user(),
              title='Stake and mushroom and sauce',
              time_minutes=5,
              price=5.00
          )
          self.assertEqual(str(recipe), recipe.title)
    ```

#### Recipe - Test

[Go Back to Contents](#contents)

- in `app/recipe/tests/test_recipe_api.py`

  ```Python
    from django.contrib.auth import get_user_model
    from django.test import TestCase
    from django.urls import reverse
    from rest_framework import status
    from rest_framework.test import APIClient
    from core.models import Recipe
    from recipe.serializers import RecipeSerializer

    RECIPES_URL = reverse('recipe:recipe-list')


    def sample_recipe(user, **params):
        """Create and return a sample recipe"""
        defaults = {
            'title': 'Sample recipe',
            'time_minutes': 10,
            'price': 5.00
        }
        defaults.update(params)
        # .update() - python function to override object
        return Recipe.objects.create(user=user, **defaults)


    class PublicRecipeApiTests(TestCase):
        """Test unauthenticated recipe API access"""

        def setUp(self):
            self.client = APIClient()

        def test_auth_required(self):
            """Test that authentication is required"""
            res = self.client.get(RECIPES_URL)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    class PrivateRecipeApiTests(TestCase):
        """Test authenticated recipe API access"""

        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                'test@test.com',
                'password123'
            )
            self.client.force_authenticate(self.user)

        def test_retrive_recipes(self):
            """Test retrieving a list of recipes"""
            sample_recipe(user=self.user)
            sample_recipe(user=self.user)
            res = self.client.get(RECIPES_URL)
            recipes = Recipe.objects.all().order_by('-id')
            serializer = RecipeSerializer(recipes, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_recipes_limited_to_user(self):
            """Test retrieving recipes for user"""
            user2 = get_user_model().objects.create_user(
                'user2@test.com',
                'password123'
            )
            sample_recipe(user=user2)
            sample_recipe(user=self.user)
            res = self.client.get(RECIPES_URL)
            recipes = Recipe.objects.filter(user=self.user)
            serializer = RecipeSerializer(recipes, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.data, serializer.data)

        def test_view_recipe_detail(self):
            """Test viewing a recipe detail"""
            recipe = sample_recipe(user=self.user)
            recipe.tags.add(sample_tag(user=self.user))
            recipe.ingredients.add(sample_ingredient(user=self.user))
            # + Add a tag and ingredient to a many to many field
            # + first we get the main object (recipe), then we add
            # + a tag/ingredient
            url = detail_url(recipe.id)
            res = self.client.get(url)
            serializer = RecipeDetailSerializer(recipe)
            # + We are serializering only one object, that why we don't need to
            # + add many=True
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_create_basic_recipe(self):
            """Test creating recipe"""
            payload = {
                'title': 'Chocolate chessecake',
                'time_minutes': 30,
                'price': 5.00
            }
            res = self.client.post(RECIPES_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            recipe = Recipe.objects.get(id=res.data['id'])
            for key in payload.keys():
                self.assertEqual(payload[key], getattr(recipe, key))
                # we need to loop through the recipe response to check
                # if the fields are correct
                # getattr() is a helper funcion builtin Python to check
                # if the property exists, if yes return the value
                # https://docs.python.org/3/library/functions.html#getattr

        def test_create_recipe_with_tags(self):
            """Test creating a recipe with tags"""
            tag1 = sample_tag(user=self.user, name="Veggan")
            tag2 = sample_tag(user=self.user, name="Dessert")
            payload = {
                'title': 'Avocado lime cheesecake',
                'tags': [tag1.id, tag2.id],
                'time_minutes': 60,
                'price': 20.00
            }
            res = self.client.post(RECIPES_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            recipe = Recipe.objects.get(id=res.data['id'])
            # get a specific recipe by id
            tags = recipe.tags.all()
            # returns all the tags associated to this recipe
            self.assertEqual(tags.count(), 2)
            self.assertIn(tag1, tags)
            self.assertIn(tag2, tags)

        def test_create_recipe_with_ingredients(self):
            """Test creating a recipe with ingredients"""
            ingredient1 = sample_ingredient(user=self.user, name='Prawns')
            ingredient2 = sample_ingredient(user=self.user, name='Ginger')
            payload = {
                'title': 'Thai prawn red curry',
                'ingredients': [ingredient1.id, ingredient2.id],
                'time_minutes': 20,
                'price': 7.00
            }
            res = self.client.post(RECIPES_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            recipe = Recipe.objects.get(id=res.data['id'])
            ingredients = recipe.ingredients.all()
            self.assertEqual(ingredients.count(), 2)
            self.assertIn(ingredient1, ingredients)
            self.assertIn(ingredient2, ingredients)

        def test_partial_update_recipe(self):
            """Test updating a recipe with patch"""
            recipe = sample_recipe(user=self.user)
            recipe.tags.add(sample_tag(user=self.user))
            new_tag = sample_tag(user=self.user, name="Curry")
            payload = {
                'title': 'Chicken tikka',
                'tags': [new_tag.id]
            }
            url = detail_url(recipe.id)
            self.client.patch(url, payload)
            recipe.refresh_from_db()
            self.assertEqual(recipe.title, payload['title'])
            tags = recipe.tags.all()
            self.assertEqual(len(tags), 1)
            self.assertIn(new_tag, tags)

        def test_full_update_recipe(self):
            """Test updating a recipe with pu"""
            recipe = sample_recipe(user=self.user)
            recipe.tags.add(sample_tag(user=self.user))
            payload = {
                'title': 'Spaghetti carbonara',
                'time_minutes': 25,
                'price': 5.00
            }
            url = detail_url(recipe.id)
            self.client.put(url, payload)

            recipe.refresh_from_db()
            self.assertEqual(recipe.title, payload['title'])
            self.assertEqual(recipe.time_minutes, payload['time_minutes'])
            self.assertEqual(recipe.price, payload['price'])
            tags = recipe.tags.all()
            self.assertEqual(len(tags), 0)
  ```

##### RECIPE - IMAGE UPLOAD TEST

[Go Back to Contents](#contents)

- in `app/core/tests/test_models.py`

  - Let's test the image upload file name
  - Import **patch** from `unittest.mock`
    - So we can mock the `uuid` to generate the same id

  ```Python
    from django.test import TestCase
    from django.contrib.auth import get_user_model
    from unittest.mock import patch
    from core import models


    def sample_user():
        """Create a sample user"""
        user = {
            "email": "test@test.com",
            "password": "test123",
            "name": "test"
        }
        return get_user_model().objects.create(**user)


    class ModelTests(TestCase):

        ...

        @patch('uuid.uuid4')
        # + we are going to patch the uuid4 function that comes from uuid
        def test_recipe_file_name_uuid(self, mock_uuid):
            """Test that image is saved in the correct location"""
            uuid = 'test-uuid'
            mock_uuid.return_value = uuid
            file_path = models.recipe_image_file_name_path(None, 'mayimage.jpg')
            # + we are going to use our custom recipe_image_file_name_path function
            # + the first argument is the instance, in our case we can pass None
            # + the second argument is the name of the file
            expected_path = f'uploads/recipe/{uuid}.jpg'
            self.assertEqual(file_path, expected_path)
  ```

- in `app/core/models.py`

  - Import **uuid** and **os**
    - **uuid** will be responsible for creating an unique id
    - **os** will be responsible to generate a valid path
  - Create our helper function `recipe_image_file_name_path`
  - Add the image field

    ```Python
      from django.db import models
      from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
          PermissionsMixin
      from django.conf import settings
      import uuid
      import os


      # this helper function will be responsible for converting the original
      # filename into an unique filename
      def recipe_image_file_name_path(instance, filename):
          # the first argument is the instance that is creating the path
          # filename is the name of the file.extension
          """Generate file path for new recipe image"""
          extension = filename.split('.')[-1]
          filename = f'{uuid.uuid4()}.{extension}'
          return os.path.join('uploads/recipe/', filename)


      ...

      class Recipe(models.Model):
          """Recipe object"""
          user = models.ForeignKey(
              settings.AUTH_USER_MODEL,
              on_delete=models.CASCADE
          )
          title = models.CharField(max_length=255)
          time_minutes = models.IntegerField()
          price = models.DecimalField(max_digits=5, decimal_places=2)
          link = models.CharField(max_length=255, blank=True)
          ingredients = models.ManyToManyField('Ingredient')
          tags = models.ManyToManyField('Tag')
          image = models.ImageField(null=True, upload_to=recipe_image_file_name_path)
          # + null=True, images are optional
          # upload_to references our recipe_image_file_name_path function
          # the upload_to function is called by the ImageField, so everytime django
          # call this field, it runs the our custom function in the background

          def __str__(self):
              return self.title
    ```

- Adding more feature to the upload image file

  - in `app/recipe/tests/test_recipe_api.py`
    - Import **tempfile**
      - This is a builtin django module that allow us to generate temporary files
      - The idea is to create a temp file, use it, and then delete it.
    - Import **os**
      - The **os** module will help us to create path names and check if the file exists
    - Import **Image** from `PIL`
    - Create a new function to automatically generate the image url

  ```Python
    from django.contrib.auth import get_user_model
    from django.test import TestCase
    from django.urls import reverse
    from rest_framework import status
    from rest_framework.test import APIClient
    from core.models import Recipe, Tag, Ingredient
    from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
    import tempfile
    import os
    from PIL import Image

    RECIPES_URL = reverse('recipe:recipe-list')

    # ! /api/recipe/recipes/1 - Details (-detail)
    def detail_url(recipe_id):
        """Return recipe detail url"""
        return reverse('recipe:recipe-detail', args=[recipe_id])
        # Using the reverse function to generate the url
        # To access a specific recipe we need to use '-detail'
        # And add the args = [recipe_id]


    def image_upload_url(recipe_id):
        """Return URL for recipe image upload"""
        return reverse('recipe:recipe-upload-image', args=[recipe_id])

    ...

    class RecipeImageUploadTests(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                'test@test.com',
                'password123'
            )
            self.client.force_authenticate(self.user)
            self.recipe = sample_recipe(user=self.user)

        # Delete the image after each test
        def tearDown(self):
            """Clean up files"""
            self.recipe.image.delete()

        def test_upload_image_to_recipe(self):
            """Test uploading an image to recipe"""
            url = image_upload_url(self.recipe.id)
            with tempfile.NamedTemporaryFile(suffix='.jpg') as name_temporary_file:
                img = Image.new('RGB', (10, 10))
                # Create a black square image
                img.save(name_temporary_file, format='JPEG')
                name_temporary_file.seek(0)
                res = self.client.post(
                    url, {'image': name_temporary_file}, format='multipart')
                self.recipe.refresh_from_db()
                self.assertEqual(res.status_code, status.HTTP_200_OK)
                self.assertIn('image', res.data)
                self.assertTrue(os.path.exists(self.recipe.image.path))

        def test_upload_image_bad_request(self):
            """Test uploading an invalid image"""
            url = image_upload_url(self.recipe.id)
            res = self.client.post(url, {'image': 'notimage'}, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  ```

- Update serializer

  - in `app/recipe/serializers.py`

    - Create a new serializer to handle the image upload

      ```Python
        from rest_framework import serializers
        from core.models import Tag, Ingredient, Recipe


        ...

        class RecipeImageSerializer(serializers.ModelSerializer):
            """Serializer for uploading images for recipes"""
            class Meta:
                model = Recipe
                fields = ('id', 'name')
                read_only_fields = ('id',)
      ```

- View (controllers)

- in `app/recipe/views.py`

  - Import **actions** from `rest_framework.decorators`
    - The **action** is responsible for creating custom action to your viewset
  - Import **Response** from `rest_framework.response`
    - To create custom JSON response
  - Update our `get_serializer_class` to handle if `self.action` is equal to `upload_image`
    - If `yes`, use `serializers.RecipeImageSerializer`

  ```Python
    from rest_framework import viewsets, mixins, status
    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.decorators import action
    # + the action is responsible for creating custom action to your viewset
    from rest_framework.response import Response
    # + returns a custom response
    from core.models import Tag, Ingredient, Recipe
    from recipe import serializers


    class BaseRecipeViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
        ...


    class TagViewSet(BaseRecipeViewSet):
        ...


    class IngredientViewSet(BaseRecipeViewSet):
        ...

    class RecipeViewSet(viewsets.ModelViewSet):
        ...

        def get_queryset(self):
            ...

        def get_serializer_class(self):
            """Return appropriate serializer class"""
            if self.action == 'retrieve':
                return serializers.RecipeDetailSerializer
            elif self.action == 'upload_image':
                return serializers.RecipeImageSerializer
            return self.serializer_class

        def perform_create(self, serializer):
            ...

        # + Custom function (custom action)
        # + we user the action decoration, then we have to define the methods that we want to allow
        # + detail=True = this means that django only is going to user this action
        # + for the detail urls, the detail in this case is a specific recipe (id=1)
        # + We are only going to be able to upload image for recipes that already exists
        # + url_path = is the path of our url
        # + localhost:8000/api/recipe/recipes/1/upload-image/
        @action(methods=['POST'], detail=True, url_path='upload-image')
        def upload_image(self, request, pk=None):
            # we need to forward the request and pk
            """Upload an image to a recipe"""
            # this will get the get object by the id that is being passed on the url
            recipe = self.get_object()
            # then we need to pass the recipe object and the data that we want to serialize
            serializer = self.get_serializer(
                recipe, data=request.data
            )
            # if the serializer is valid, then save
            if serializer.is_valid():
                serializer.save()
                # + Create our custom response
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            # + Create our custom response
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
  ```

#### Recipe - Filter

##### RECIPE - VIEWS (CONTROLLERS)

[Go Back to Contents](#contents)

- in `app/recipe/views.py

  - Create a private helper funciton to convert the query string into a list of number
    - `_` - it's not really private, but the convention is to use `_` to identify as private
  - before we return the filter objects by user

    - we will convert the query string into a list
    - filter the filter the objects by foreginkey
    - then filter the objecs by user

      ```Python
        from rest_framework import viewsets, mixins, status
        from rest_framework.authentication import TokenAuthentication
        from rest_framework.permissions import IsAuthenticated
        from rest_framework.decorators import action
        from rest_framework.response import Response
        from core.models import Tag, Ingredient, Recipe
        from recipe import serializers

        ...

        class RecipeViewSet(viewsets.ModelViewSet):
            """Manage recipes in the database"""
            serializer_class = serializers.RecipeSerializer
            queryset = Recipe.objects.all()
            authentication_classes = (TokenAuthentication,)
            permission_classes = (IsAuthenticated,)

            def _params_to_integer(self, query_string):
                """Convert a list of string ID to a list of integers"""
                return [int(str_id) for str_id in query_string.split(',')]

            def get_queryset(self):
                """Retrieve the recipes for the authenticated user"""
                # filter by tag and ingredients
                # we can use the query_params that comes with the request
                # the query_params returns a dictionary (object), then we can use
                # .get('key') to get the value
                # if the 'key' is not provided, the .get() will return None
                tags = self.request.query_params.get('tags')
                ingredients = self.request.query_params.get('ingredients')
                queryset = self.queryset
                # then we are going to modify the queryset, then we will return the
                # the modified queryset
                if tags:
                    tag_ids = self._params_to_integer(tags)
                    queryset = queryset.filter(tags__id__in=tag_ids)
                    # django syntax to filter the foreginkeys
                    # field__foreginkey__in
                    # filed = tags' filed in our queryset
                    # __id  = foreginkey to tag's table
                    # __in  = apply a function "in"
                    #         Return all the objects where the id is in this list
                if ingredients:
                    ingredient_ids = self._params_to_integer(ingredients)
                    queryset = queryset.filter(ingredients__id__in=ingredient_ids)
                return queryset.filter(user=self.request.user)

            def get_serializer_class(self):
                ...

            def perform_create(self, serializer):
                """Create a new recipe"""
                serializer.save(user=self.request.user)

            @action(methods=['POST'], detail=True, url_path='upload-image')
            def upload_image(self, request, pk=None):
                ...
      ```

- in `app/recipe/views.py`

  - After creting the filter test for **tags** and **ingredients**
  - We need to update the view to handle the modifications
  - We need to update our **BaseRecipeViewSet** to handle the filter

    ```Python
      ...

      class BaseRecipeViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
          ...

          def get_queryset(self):
              """Return object for the authenticated user only"""
              assigned_only = bool(
                  int(self.request.query_params.get('assigned_only', 0)))
              # returns only the objects that have tags/ingredients assigned
              # if assigned_only doesn't exist, then 0 is the default value
              queryset = self.queryset
              if assigned_only:
                  queryset = queryset.filter(recipe__isnull=False)
              return queryset.filter(user=self.request.user).order_by("-name").distinct()
              # distinct only returns uniques objects (exclude duplicates)

          def perform_create(self, serializer):
              ...
    ```

##### RECIPE - TEST FILTER

[Go Back to Contents](#contents)

- in `app/recipe/tests/test_recipe_api.py`

  ```Python
    ...

    class RecipeImageUploadTests(TestCase):
        ...

        def test_filter_recipes_by_tags(self):
            """Test returning recipes with specific tags"""
            recipe1 = sample_recipe(
                user=self.user,
                title='Thai vegetable curry',
            )
            recipe2 = sample_recipe(
                user=self.user,
                title='Aubergine with tahini',
            )
            tag1 = sample_tag(user=self.user, name='Vegan')
            tag2 = sample_tag(user=self.user, name='Vegetarian')
            recipe1.tags.add(tag1)
            recipe2.tags.add(tag2)
            recipe3 = sample_recipe(
                user=self.user,
                title="Fish and chips"
            )
            res = self.client.get(
                RECIPES_URL,
                {'tags': f'{tag1.id},{tag2.id}'
                }
            )
            serializer1 = RecipeSerializer(recipe1)
            serializer2 = RecipeSerializer(recipe2)
            serializer3 = RecipeSerializer(recipe3)
            self.assertIn(serializer1.data, res.data)
            self.assertIn(serializer2.data, res.data)
            self.assertNotIn(serializer3.data, res.data)

        def test_filter_recipes_by_ingredients(self):
            """Test returning recipes with specific ingredients"""
            recipe1 = sample_recipe(
                user=self.user,
                title="Posh beans on toast"
            )
            recipe2 = sample_recipe(
                user=self.user,
                title="Chicken cacciatore"
            )
            ingredient1 = sample_ingredient(
                user=self.user,
                name="Feta cheese"
            )
            ingredient2 = sample_ingredient(
                user=self.user,
                name="Chicken"
            )
            recipe1.ingredients.add(ingredient1)
            recipe2.ingredients.add(ingredient2)
            recipe3 = sample_recipe(
                user=self.user,
                title="Steak and mushroom"
            )
            res = self.client.get(
                RECIPES_URL,
                {'ingredients': f'{ingredient1.id},{ingredient2.id}'}
            )
            serializer1 = RecipeSerializer(recipe1)
            serializer2 = RecipeSerializer(recipe2)
            serializer3 = RecipeSerializer(recipe3)
            self.assertIn(serializer1.data, res.data)
            self.assertIn(serializer2.data, res.data)
            self.assertNotIn(serializer3.data, res.data)
  ```

##### TAG - TEST FILTER

[Go Back to Contents](#contents)

- in `app/recipe/tests/test_tags_api.py`

  ```Python
    from core.models import Tag, Recipe

    ...

    class PrivateTagsApiTests(TestCase):
        ...

        def test_retrive_tags_assigned_to_recipes(self):
            """Test filtering tags by those assigned to recipes"""
            tag1 = Tag.objects.create(
                user=self.user,
                name="Breakfast"
            )
            tag2 = Tag.objects.create(
                user=self.user,
                name="Lunch"
            )
            recipe = Recipe.objects.create(
                title="Coriander eggs on toast",
                time_minutes=10,
                price=5.00,
                user=self.user
            )
            recipe.tags.add(tag1)
            res = self.client.get(
                TAGS_URL,
                {
                    'assigned_only': 1
                }
            )
            serializer1 = TagSerializer(tag1)
            serializer2 = TagSerializer(tag2)
            self.assertIn(serializer1.data, res.data)
            self.assertNotIn(serializer2.data, res.data)

        def test_retrieve_tags_assigned_unique(self):
            """Test filtering tags by assigned returns unique items"""
            tag = Tag.objects.create(
                user=self.user,
                name='Breakfast'
            )
            Tag.objects.create(
                user=self.user,
                name='Lunch'
            )
            recipe1 = Recipe.objects.create(
                title='Pancakes',
                time_minutes=5,
                price=3.00,
                user=self.user
            )
            recipe1.tags.add(tag)
            recipe2 = Recipe.objects.create(
                title='Porridge',
                time_minutes=3,
                price=2.00,
                user=self.user
            )
            recipe2.tags.add(tag)
            res = self.client.get(
                TAGS_URL,
                {
                    'assigned_only': 1
                }
            )
            self.assertEqual(len(res.data), 1)
  ```

##### INGREDIENT - TEST FILTER

[Go Back to Contents](#contents)

- in `app/recipe/tests/test_ingredients_api.py`

  ```Python
    from core.models import Ingredient, Recipe

    ...

    class PrivateIngredientsApiTests(TestCase):
        ...

        def test_retrive_ingredients_assigned_to_recipes(self):
            """Test filtering ingredients by those assigned to recipes"""
            ingredient1 = Ingredient.objects.create(
                user=self.user,
                name="Apples"
            )
            ingredient2 = Ingredient.objects.create(
                user=self.user,
                name="Turkey"
            )
            recipe = Recipe.objects.create(
                title="Apple crumble",
                time_minutes=5,
                price=10,
                user=self.user
            )
            recipe.ingredients.add(ingredient1)
            res = self.client.get(
                INGREDIENTS_URL,
                {
                    'assigned_only': 1
                }
            )
            serializer1 = IngredientSerializer(ingredient1)
            serializer2 = IngredientSerializer(ingredient2)
            self.assertIn(serializer1.data, res.data)
            self.assertNotIn(serializer2.data, res.data)

        def test_retrieve_ingredients_assigned_unique(self):
            """Test filtering ingredients by assigned returns unique items"""
            ingredient = Ingredient.objects.create(
                user=self.user,
                name="Eggs"
            )
            Ingredient.objects.create(
                user=self.user,
                name="Cheese"
            )
            recipe1 = Recipe.objects.create(
                title="Eggs benedict",
                time_minutes=30,
                price=12.00,
                user=self.user
            )
            recipe1.ingredients.add(ingredient)
            recipe2 = Recipe.objects.create(
                title="Coriander eggs on toast",
                time_minutes=20,
                price=5.00,
                user=self.user
            )
            recipe2.ingredients.add(ingredient)
            res = self.client.get(
                INGREDIENTS_URL,
                {
                    "assigned_only": 1
                }
            )
            self.assertEqual(len(res.data), 1)
  ```
