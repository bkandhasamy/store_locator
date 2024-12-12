from invoke import task


@task
def start(ctx):
    """Run the FastAPI application"""
    ctx.run("uvicorn store_locator.main:store_locator --reload")


@task
def test(ctx):
    """Run all tests with coverage"""
    ctx.run("pytest --cov=store_locator tests/")


@task
def lint(ctx):
    """Run linters and code quality checks"""
    ctx.run("black .")
    ctx.run("flake8 .")
    ctx.run("mypy store_locator/")


@task
def docker_up(ctx):
    """Bring up the Docker environment"""
    ctx.run("docker-compose up -d")


@task
def docker_down(ctx):
    """Shut down the Docker environment"""
    ctx.run("docker-compose down")


@task
def clean(ctx):
    """Clean up the environment"""
    ctx.run("find . -type d -name '__pycache__' -exec rm -r {} +")


@task
def benchmark(ctx):
    """Run locust benchmark"""
    ctx.run("locust -f locustfile.py --host=http://localhost:8000")
