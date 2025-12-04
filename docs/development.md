# Development Guide

This guide covers common development tasks for the networkx-mermaid project.

## Setup

Install the project with development dependencies:

```shell
uv pip install -e ".[dev,test,docs]"
```

## Running Tests

Run tests using pytest:

```shell
pytest tests
```

Run tests with coverage:

```shell
pytest tests --cov=src --cov-branch --cov-report=html
```

Run tests in parallel:

```shell
pytest tests -n auto
```

Run tests including README examples:

```shell
pytest tests README.md
```

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and code formatting.

Check for linting issues:

```shell
ruff check .
```

Fix auto-fixable linting issues:

```shell
ruff check --fix .
```

Format code:

```shell
ruff format .
```

## Type Checking

This project uses [mypy](https://mypy-lang.org/) for static type checking.

Run type checking:

```shell
mypy src
```

## Documentation

Documentation is built using [zensical](https://zensical.org), an Open Source documentation system built by the creators of Material for MkDocs.

Serve documentation locally:

```shell
zensical serve
```

Build documentation:

```shell
zensical build
```

The documentation will be built to the `site/` directory.

Configuration is managed in `zensical.toml`.

## Development Workflow

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run linting: `ruff check . && ruff format .`
4. Run type checking: `mypy src`
5. Run tests: `pytest tests --cov=src`
6. Commit your changes
7. Push and create a pull request

## Project Structure

```
networkx-mermaid/
├── docs/                 # Documentation files
├── src/                  # Source code
├── tests/                # Test files
├── LICENSE               # License information
├── pyproject.toml        # Project configuration
├── README.md             # Project description
└── zensical.toml         # Zensical configuration

```
