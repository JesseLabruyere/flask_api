# manual install

## update
$ apt-get update

## pip
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade virtualenv

## new virtual env
$ mkdir flask_project
$ cd flask_project
$ virtualenv venv

## activate the virtual env, from project folder ~/flask_project
$ . venv/bin/activate

## install flask
$ pip install Flask

## installing libraries
### Installing yml support
$ easy_install pip
$ pip install pyyaml
### Check if library is installed
$ python -c "import werkzeug"
### 0 means success 1 means fail
$ echo $?