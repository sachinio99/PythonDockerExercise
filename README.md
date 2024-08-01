# Python with Docker




This project implements a command line interface to extract code snippets from a
markdown file and execute them. See Open PR 

## TO DO

Write a script that allows executing the Python snippets in a `.md` with any given
Python version. The script should take the path of the `.md` file to run and
the Python version to use. Execution must be done in a Docker container.

```sh
python run-with-version.py examples/print-python-version.md --version 3.10
python run-with-version.py examples/print-python-version.md --version 3.11
```

## Evaluation criteria

## Guidelines

- Each code chunk should have access to previously defined variables (e.g., `print(x)` in chunk 2 should work if chunk 1 has `x = 1`, see [`examples/print-python-version.md`](examples/print-python-version.md) for an example)
- You can use any docker image you want (even public ones)
- You can assume the `python run-with-version.py` command will be executed in the root folder of this project
- The script should spin up and shut down the container, do not assume a container is already running
- For a good user experience consider adding documentation, validate user input, and display clear error messages



You can run `python -m build` (this uses the [`build`](https://github.com/pypa/build) package, which you can install via `pip install build`) to generate a tarball of this project. Then, you can install the project as a Python package with:

```sh
pip install path/to/tarball.tar.gz
```



## Installation


```sh
pip install invoke

# this will create a conda environment, install ploomber_test as a package
# and install all required dependencies to run the code
invoke setup
```

## Testing

```sh
# ensure you activate the environment
conda activate ploomber-test

# run tests
pytest
```

If all is working correctly, you'll see something like this:

```
================================= test session starts ==================================
platform darwin -- Python 3.10.12, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/eduardo/dev/take-home-test
configfile: pyproject.toml
collected 12 items

tests/test_parse.py ...                                                          [ 25%]
tests/test_runner.py ........Xx                                                  [100%]

======================= 11 passed, 1 xfailed, 1 xpassed in 6.56s =======================
```

The CLI should work now:

```sh
# ensure you activate the environment
conda activate ploomber-test

ploomber-test --help
```

```
Usage: ploomber-test [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run
```

You can run some examples:

```sh
ploomber-test run examples/print-python-version.md

ploomber-test run examples/sql-query.md
```

`ploomber-test` will run the `.md` file in the current environment, you can use this
as a starting point to build your solution (which should run the code in a Docker
container).


## Editing the code

The `invoke setup` command sets up your environment, so you should now be ready to
code.

To verify that everything is working correctly, you can run the following command:

```sh
python -c "import ploomber_test; print(ploomber_test)"
```

You should see something like this:

```
<module 'ploomber_test' from '/path/to/take-home-test/src/ploomber_test/__init__.py'>
```

Where `/path/to/take-home-test/` is the directory where this code is located.

Try making a change to `cli.py`:

```python
@click.group()
def cli():
    print("hello from cli!") # add this
```

Then, run one of the examples:

```sh
ploomber-test run examples/print-python-version.md
```

You should see that your changes are reflected:

```
hello from cli!
Running: {'code': 'import sys\nprint(sys.version)', 'language': 'python'}
3.10.12 (main, Jul  5 2023, 15:02:25) [Clang 14.0.6 ]
Output: None
Running: {'code': '1 + 1', 'language': 'python'}
Out[1]: 2
Output: 2
```

## Troubleshooting

If you're having issues with the `invoke setup` command, you can follow these steps:

```sh
# create a new conda environment (you can also use any other virtual environment tool
# like venv or virtualenv)
conda create --name ploomber-test python=3.10 --yes

# activate environment
conda activate ploomber-test

# install project in editable mode (run this from the root directory as this command
# will look for the setup.py file)
pip install --editable ".[dev]"
```

To verify the installation:

```sh
# run unit tests
pytest

# run an example using the CLI
ploomber-test run examples/print-python-version.md

# check the package was correctly installed in editable mode
python -c "import ploomber_test; print(ploomber_test)"
# should print something like:
# <module 'ploomber_test' from '/path/to/take-home-test/src/ploomber_test/__init__.py'>
```
