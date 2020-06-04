"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import platform
import shutil
import webbrowser
from pathlib import Path

from invoke import task  # type: ignore
from invoke.runners import Failure, Result  # type: ignore

ROOT_DIR = Path(__file__).parent
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("yamldataclassconfig")
SETUP_PY = ROOT_DIR.joinpath("setup.py")
TASKS_PY = ROOT_DIR.joinpath("tasks.py")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SETUP_PY, TASKS_PY, SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


@task(help={"check": "Checks if source is formatted without applying changes"})
def style(context, check=False):
    """
    Format code
    """
    for result in [
        isort(context, check),
        pipenv_setup(context, check),
        black(context, check),
    ]:
        if result.failed:
            raise Failure(result)


def isort(context, check=False) -> Result:
    """Runs isort."""
    isort_options = "--recursive {}".format("--check-only --diff" if check else "")
    return context.run("isort {} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True)


def pipenv_setup(context, check=False) -> Result:
    """Runs pipenv-setup."""
    isort_options = "{}".format("check --strict" if check else "sync --pipfile")
    return context.run("pipenv-setup {}".format(isort_options), warn=True)


def black(context, check=False) -> Result:
    """Runs black."""
    black_options = "{}".format("--check --diff" if check else "")
    return context.run("black {} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True)


@task
def lint_flake8(context):
    """
    Lint code with flake8
    """
    context.run("flake8 {} {}".format("--radon-show-closures", " ".join(PYTHON_DIRS)))


@task
def lint_pylint(context):
    """
    Lint code with pylint
    """
    context.run("pylint {}".format(" ".join(PYTHON_DIRS)))


@task
def lint_mypy(context):
    """
    Lint code with pylint
    """
    context.run("mypy {}".format(" ".join(PYTHON_DIRS)))


@task(lint_flake8, lint_pylint, lint_mypy)
def lint(_context):
    """
    Run all linting
    """


@task
def radon_cc(context):
    """
    Reports code complexity.
    """
    context.run("radon cc {}".format(" ".join(PYTHON_DIRS)))


@task
def radon_mi(context):
    """
    Reports maintainability index.
    """
    context.run("radon mi {}".format(" ".join(PYTHON_DIRS)))


@task(radon_cc, radon_mi)
def radon(_context):
    """
    Reports radon.
    """


@task
def xenon(context):
    """
    Check code complexity.
    """
    context.run(("xenon" " --max-absolute A" "--max-modules A" "--max-average A" "{}").format(" ".join(PYTHON_DIRS)))


@task
def test(context):
    """
    Run tests
    """
    pty = platform.system() == "Linux"
    context.run("python {} test".format(SETUP_FILE), pty=pty)


@task(help={"publish": "Publish the result via coveralls", "xml": "Export report as xml format"})
def coverage(context, publish=False, xml=False):
    """
    Create coverage report
    """
    context.run("coverage run --source {} -m pytest".format(SOURCE_DIR))
    context.run("coverage report -m")
    if publish:
        # Publish the results via coveralls
        context.run("coveralls")
        return
    # Build a local report
    if xml:
        context.run("coverage xml")
    else:
        context.run("coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task
def clean_build(context):
    """
    Clean up files from package building
    """
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    context.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(context):
    """
    Clean up python file artifacts
    """
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    context.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(_context):
    """
    Clean up files from testing
    """
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests])
def clean(_context):
    """
    Runs all clean sub-tasks
    """


@task(clean)
def dist(context):
    """
    Build source and wheel packages
    """
    context.run("python setup.py sdist")
    context.run("python setup.py bdist_wheel")
