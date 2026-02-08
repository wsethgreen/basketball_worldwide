# Basketball Worldwide

Basketball Worldwide API built with FastAPI. We use `uv` for dependency management and `docker compose` for running the app alongside Postgres.

### Depedencies
- Python 3.13+
  - Note: It's recommended to install Python 3.13+ using uv's [Python installation functionality](https://docs.astral.sh/uv/guides/install-python/).
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)

### Local Setup (uv)
1. Create and sync the environment in the root directory:
   ```bash
   uv sync
   ```
2. (Optional) Run the API locally:
   ```bash
   uv run src/main.py
   ```
   - It's recommended you run the app via docker compose.

### Running the App locally
1. Build and run the app via docker compose:
   ```bash
   docker compose up --build
   ```
2. Stop and tear down containers:
   ```bash
   docker compose down
   ```

### Linting and Formatting
This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. Ruff is included as a dev dependency on the project.
The linter and formatter run automatically during a commit via `pre-commit`. See pre-commit section for setting up pre-commit.

You can optionally run the linter and formatter locally at any time.

1. To run the linter against all python files:
    ```bash
    uv run ruff check
    ```
2. To run the formatter against all python files:
    ```bash
    uv run ruff format
    ```


#### Pre-commit

We use [pre-commit](https://pre-commit.com/) to run the `ruff` linter and formatter on stages files on commits. 
Pre-commit is included as a dev dependency on this project.

Set up `pre-commit` in this repo:
1. Install hooks:
   ```bash
   uv run pre-commit install
   ```
2. (Optional) Run against all files:
   ```bash
   uv run pre-commit run --all-files
   ```
