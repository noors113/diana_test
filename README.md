# EventHub

## Installation

### Clone the repository:

```shell
git clone https://github.com/noors113/diana_test.git
```

### Copy env file

```shell
cp .env.template .env
```

### Install dependencies

```shell
poetry install
```

If you don't have poetry installed, please read
the [Documentation](https://python-poetry.org/docs/#installation)

```shell
pre-commit install
```

If you don't have pre-commit installed, please read
the [Documentation](https://pre-commit.com/#install)

### Configure services

I suggest to use docker-compose to up needed services except the application
itself

```shell
docker-compose up <service_name_1> <service_name_2> -d
```
