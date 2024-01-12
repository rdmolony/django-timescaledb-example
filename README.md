# Django TimescaleDB Example

This example uses ...

- `Django` as the “glue” between web browsers and a database[^DJANGO]

- `Postgres` with extension `TimescaleDB` as the web application database[^TIMESCALEDB]

- `Celery` as a task queue powered by `Redis`

> [!TIP]
> If you have any trouble getting setup,  feel free to ask a question at [django-timescaledb-example/discussions](https://github.com/rdmolony/django-timescaledb-example/discussions)

---


## Installation

- [Clone this repository locally](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)[^GITHUB]

- Install [`Python`](https://www.python.org/)[^PYTHON] & [`pipx`](https://github.com/pypa/pipx)[^PIPX] and thus [`poetry`](https://github.com/python-poetry/poetry)[^POETRY] & [`honcho`](https://github.com/nickstenning/honcho)[^HONCHO]

- Install [`Postgres`](https://www.postgresql.org/)[^POSTGRES] and thus [`TimescaleDB`](https://www.timescale.com/)[^POSTGRES]

- Install [`Redis`](https://redis.io/)[^REDIS]

> [!IMPORTANT]  
> For `Windows` try [`tporadowski/redis`](https://github.com/tporadowski/redis) or [`zkteco-home/redis-windows`](https://github.com/zkteco-home/redis-windows).  `Celery` is used alongside `Redis` as a task queue & may not run in which case you'll have to adapt `**/tasks.py` for [`Bogdanp/dramatiq`](https://github.com/Bogdanp/dramatiq)

- Install this project's `Python` dependencies via ...

    ```sh
    poetry install
    ```

- Create a `.env` file from `.env.dist` **to store credentials** ...

    ```sh
    cp .env.dist .env
    ```

> [!WARNING]  
> **Create a complex secret key**[^SECRET_KEY] if you intend to deploy this web application

- Create a `TimescaleDB` database with user `django` via the `Postgres` CLI ...

    ```sh
    sh shell/createdb.sh
    ```

> [!IMPORTANT]  
> For `Windows` adapt `shell/createdb.sh` for `Command Prompt` or `PowerShell`

> [!WARNING]  
> [**Create a new role with a password**](https://www.postgresql.org/docs/current/database-roles.html) if you go on to do something with this database

- Create a superuser to access the `admin` site ...

    ```sh
    poetry run python manage.py createsuperuser 
    ```


---


## Run

- Launch `Django`, `Redis` & `Celery` ...

    ```sh
    honcho start
    ```

> [!TIP]  
> Go to [`http://localhost:8000`](http://localhost:8000) & you should see a running web application


---


## How to ...

- Re-launch the database server ...

```sh
pg_ctl start -D .db/
```

- Launch a shell within your virtual environment so you don't need `poetry run`** to run `Django` commands like `poetry run python manage.py ...` ...

```sh
poetry shell
```


---


<details>
<summary>Footnotes</summary>

[^DJANGO]: To display a web page it asks a database for the data it needs to render files that the browser interprets (HTML, CSS & JavaScript) so it can display a user interface

[^HONCHO]: I use `pipx` ...

    ```sh
    pipx install honcho
    ```

[^GITHUB]:

    I use [`git clone`](https://git-scm.com/) ...

    ```sh
    git clone git@github.com:rdmolony/rdmolony.github.io.git
    ```

    ... since I prefer to [authenticate with `GitHub` via `SSH`](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

[^PIPX]: I use [`nix`](https://github.com/DeterminateSystems/nix-installer) ...

    ```sh
    nix profile install nixpkgs#pipx
    ``` 

    Why not use `pip`?  `Python` ships with `pip` which installs dependencies "globally" which means that you can't easily install the same 3rd party library twice

[^POETRY]: I use `pipx` ...

    ```sh
    pipx install poetry
    ```

[^PYTHON]: I use [`nix`](https://github.com/DeterminateSystems/nix-installer) ...

    ```sh
    nix profile install nixpkgs#python3
    ```

[^POSTGRES]: I use [`nix`](https://github.com/DeterminateSystems/nix-installer) ...

    ```sh
    nix profile install --impure --expr 'with import <nixpkgs> {}; pkgs.postgresql.withPackages   (p: [ p.timescaledb ])'
    ```

[^REDIS]: I use [`nix`](https://github.com/DeterminateSystems/nix-installer) ...

    ```sh
    nix profile install nixpkgs#redis
    ```

[^SECRET_KEY]: Generate a `SECRET_KEY` ...

    ```sh
    poetry run python -c "
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    "
    ```

    ... & copy it into `.env`

[^TIMESCALEDB]: `TimescaleDB` is an extension to the `Postgres` database which grants it timeseries capabilities.  `Postgres` wasn't designed to handle timeseries workloads in which data is infrequently inserted and frequently queried in bulk.  `TimescaleDB` adapts `Postgres` via "hypertables" which enable compression of many rows into "chunks" which are indexed by timestamps.  Consequently,  queries on ranges of timestamps are faster since `Postgres` can search "chunks" instead of rows & storage is cheaper.  By compressing, `TimescaleDB` trades insert performance for query performance.
