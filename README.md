# Django development environment using VSCode Remote Containers

## Pre-requisites:

1. Docker 
2. VSCode
3. VSCode Dev Containers extension
4. VSCode Docker extension

## How to run the application

The application uses VSCode Dev Containers. [Set up your VSCode to open from the terminal](https://www.freecodecamp.org/news/how-to-open-visual-studio-code-from-your-terminal/) . Just navigate to the root of the project and in Linux use  ``` code . ``` to open VSCode , you should be prompted to open the application in a container. See [Dev Containers for more information](https://code.visualstudio.com/docs/devcontainers/containers)

You will probably be prompted to load the python extension , unfortunately this is a bug and hasn't been resolved yet, so just do it, otherwise Flake8 linting and Black formatting will not be avaliable. [See known issues](#Know-Issues)

In a terminal use ``` python manage.py run_app ``` this will open the app in a browser at http://127.0.0.1:8000/

You should see "Nice!"

## How to rename the project

A helper command rename_project has been created follow these steps

1. Run ``` python manage.py rename_project <old_name> <new_name>

2. Then rename the project.


## Details of setting up default Django project:

Create an empty app.py file in the directory. 

Open the command palette (cmd+P on Mac, Ctrl+Shift+P on Windows), and select Docker: Add Docker Files to Workspace. It should give you a number of options, including Python: Django which is the one we want. Select Python: Django. It should then ask you for the entry point, so select the app.py file we created earlier.

It will then ask you which port you want to listen to, the default is fine.

The last one should be “Include optional Docker Compose files?”, Select 'Yes'.

Delete app.py

## Add the development container definition and connecting to it:

Open your command palette, and select Dev-Containers: Add Development Container Configuration Files. You should get a prompt asking you how you would like to create your container configuration, and you should choose from docker-compose.yml. This should create a .devcontainer folder, with devcontainer.json inside it.

Open your command palette again, and select Dev-Containers: Rebuild and Reopen in Container

You should see another window open with a number of things running. This is just VSCode setting up your development container. Wait until it’s done.

## Generate your Django project:

Open a terminal if it isn't alreay open an use the commands 
``` $ django-admin startproject testproject . ```
``` $ python manage.py runserver ```

Check default page on http://127.0.0.1:8000

### Add Postgres

In your docker-compose.yml file you should add one service for Postgres. 
```

version: '3.4'

services:
  dev4containerdjango:
    image: dev4containerdjango
    build:
      context: .
      dockerfile: ./Dockerfile
    volumes:
      - ./app:/app
    environment:
      - DB_HOST=postgresdb
      - DB_NAME=devdb
      - DB_USER=dbuser
      - DB_PASS=changeme
      - DB_PORT=5432
    depends_on:
      - postgresdb

  postgresdb:
    image: postgres:15-alpine
    volumes: 
      - dev-db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=devdb
      - POSTGRES_USER=dbuser
      - POSTGRES_PASSWORD=changeme
volumes:
  dev-db-data:

```

Modify settings.py to point to the Postgres container (in production these values should ideally be read from environment variables):

```

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "CONN_MAX_AGE": 60,
    }
}

```

Add psycopg2-binary to your requirements.txt file, and pin it to the most recent version

Rebuild and reopen the container again

## Check your set up 

1. In the terminal use ``` pip freeze ``` to see dependencies
2. In terminal run ``` cat /etc/os-release ```  which should show the OS as Debian (the image OS) . This shows you are in the container. Or use ``` echo $DOCKER_RUNNING ```

## Add formatting and Linting

Add the following to the evcontainers.json (see known issue (2))

	 "customizations": {
		"vscode": {
			"settings": {
				"[python]": {
					"editor.tabSize": 4,
					"editor.formatOnSave": true,
					"editor.codeActionsOnSave": {
							"source.organizeImports": true
					}
				}
			},
			"extensions": [
				"ms-python.python",
				"ms-python.black-formatter",
				"ms-python.isort",
				"ms-python.flake8",
				"ms-azuretools.vscode-docker"
			]

   
## Know Issues:

1. Sometimes I’ve found that VSCode would fail to forward the port automatically now that we’ve published port 8000 in the docker-compose.yml, which conflicts with the port forwarding feature. In that case you should try runserver by binding to 0.0.0.0, i.e. python manage.py runserver 0.0.0.0:8000. Or alternatively, you could also just remove ports from the docker-compose.yml file as done in this example.

2. When formatting and linting are enable you will be requeste to install the Python extension of VSCode. This appears to be a bug where the extension is slow / isn't installed as it should be and the manual install is required see [GitHub Issue 1967784](https://github.com/microsoft/vscode/issues/196794)
   
   




