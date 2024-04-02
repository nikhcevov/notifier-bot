## Project setup

```sh
# 1. Install requirements
pip install pipenv
pipenv run init

# 2. Activate
pipenv shell
```

```sh
# build docker image *optional
docker build -t $(DOCKER_TAG_NAME) .
```

## Run application
```sh
# compiles and hot-reloads
pipenv run start
```

```sh
# run docker container *optional
docker container run --rm -p 5000:5000 $(DOCKER_TAG_NAME)
```

## Extras
```sh
# type check
pipenv run type
```

```sh
# lint
pipenv run lint
```

```sh
# format
pipenv run format
```