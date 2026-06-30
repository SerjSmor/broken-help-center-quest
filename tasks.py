from invoke import task


@task
def install(ctx):
    """Install the local package."""
    ctx.run('python3 -m pip install -e ".[dev]"')


@task
def data(ctx):
    """Prepare the WixQA-derived benchmark into data/processed if missing."""
    ctx.run("python3 scripts/prepare_dataset.py")
