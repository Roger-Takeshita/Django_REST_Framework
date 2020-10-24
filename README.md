<h1 id='contents'>Table of Contents</h1>

- [FOLDER AND FILES](#folder-and-files)
- [DOCKER](#docker)
  - [Docker File](#docker-file)
  - [requirements.txt](#requirementstxt)
  - [Build Docker Image](#build-docker-image)
  - [Docker Compose](#docker-compose)
    - [Docker Compose Build](#docker-compose-build)
- [DJANGO REST_FRAMEWORK](#django-rest_framework)
  - [Enable Travis CI and Flake8](#enable-travis-ci-and-flake8)
    - [Travis CI](#travis-ci)
      - [Config .travis.yml](#config-travisyml)
    - [Flake8](#flake8)
      - [Config Flake8](#config-flake8)
  - [Start New Project Using Docker](#start-new-project-using-docker)
    - [Create a New App Using Docker](#create-a-new-app-using-docker)
    - [Create Folder and Files](#create-folder-and-files)
    - [Model](#model)
      - [BaseUserManager](#baseusermanager)
      - [AbstractBaseUser](#abstractbaseuser)
      - [PermissionsMixin](#permissionsmixin)
    - [Config Auth Settings](#config-auth-settings)
    - [Migrations](#migrations)
      - [Makemigrations](#makemigrations)
      - [Migrate](#migrate)
    - [Admin Panel](#admin-panel)
  - [Tests](#tests)

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
       RUN adduser -D dockeruser
       # adduser         = create a user
       # -D              = only for running applications
       # dockeruser      = the name of the user
       USER dockeruser
       # USER dockeruser = Change the user to dockeruser
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

# DJANGO REST_FRAMEWORK

[Go Back to Contents](#contents)

## Enable Travis CI and Flake8

### Travis CI

[Go Back to Contents](#contents)

- [Travis CI Website](https://travis-ci.org/)
- [Travis CI Tutorial](https://docs.travis-ci.com/user/tutorial/)
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
    docker-compose run app sh -c "django-admin.py startproject config ."

    # docker-compose run                      = docker command to run command
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
    docker-compose run app sh -c "python manager.py startapp core"

    # docker-compose run                = docker command to run command
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

### Create Folder and Files

[Go Back to Contents](#contents)

- Create the following files using my custom [touch](https://github.com/Roger-Takeshita/Shell-Script/blob/master/touch-open.sh) command

  ```Bash
    touch app/core/tests/__init__.py + test_models.py
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
    docker-compose run app sh -c "python manager.py makemigrations"
  ```

- The output in the terminal informs us that the following migration file was created: `app/core/migrations/0001_initial.py`
- A migrations directory is created for an app the first time you run **makemigrations**.

#### Migrate

[Go Back to Contents](#contents)

- Simply creating migration files does not update the database.
- To synchronize the database's schema with the code in the migration files, we "migrate" using this command:

  ```Bash
    docker-compose run app sh -c "python manager.py migrate"
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

## Tests

[Go Back to Contents](#contents)

- To test our application, we need to import **TestCase** from `djando.test`

  - To use the test model we need to create a `test_file_name.py` or a folder called `tests`. We cannot have both on the root of our app.
  - Run the tests
    - `docker-compose run app sh -c "python manage.py test"`

- In `app/core/tests/test_models.py`

  - Import the **TestCase** from `django.test`
  - Bellow that we are going to import the `get_user_model` helper function to import our models. This is recommended because if we change our user model we will need to change all the tests that uses that model

  ```Python
    from django.test import TestCase
    from django.contrib.auth import get_user_model


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
  ```
