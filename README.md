### Simple Django Project

### Install git, gitlfs, docker

clone the repository

### vscode terminal commands for:
### build, start, stop containers
./cmd build
./cmd start
./cmd stop

### populate db
./cmd start
./cmd shell
./manage.py makemigrations
./manage.py migrate
./manage.py populate_dev_db

 -- App is run on http://localhost:8000/admin

login: simple
password: simple

### for delete db:
- stop containers
- delete "db" folder from /volumes
- start containers
- go to shell
 - make populate db


### logs check
docker logs simple
docker logs simple-db

### status check
docker ps
docker network inspect simple-network


### Git

git pull

git add .
git commit -m "your message"
git push
git checkout "branch_name"

git rebase



- All models, including internal Django models:
./manage.py graph_models -a -o docs/all_models_diagram.png

- Only models of the simple application:
./manage.py graph_models -a -o docs/simple_models_diagram.png --exclude-models LogEntry,Permission,Group,AbstractUser,PermissionMixin,ContentType,Session,DjangoJob,DjangoJobExecution,AbstractBaseSession,User,Task

- файлы с именами, заканчивающимися на _test.py, будут рассматриваться как тестовые файлы.


### Документация OpenAPI (Swagger)

Документация доступна по адресу:
[http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)
