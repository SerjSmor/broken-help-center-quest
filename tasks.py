from invoke import task


@task
def install(ctx):
    """Install the local package and development dependencies."""
    ctx.run('python3 -m pip install -e ".[dev]"')


@task
def data(ctx):
    """Prepare the WixQA-derived benchmark into data/processed."""
    ctx.run("python3 scripts/prepare_dataset.py")


@task
def test(ctx):
    """Run the automated test suite."""
    ctx.run("python3 -m pytest")


@task
def tour(ctx):
    """Run the Streamlit data tour."""
    ctx.run("python3 -m streamlit run tools/data_tour.py")
