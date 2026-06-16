from __future__ import annotations

from typing import Annotated

import typer

from buildguild.status import print_status


app = typer.Typer(no_args_is_help=True)
run_app = typer.Typer(no_args_is_help=True)
app.add_typer(run_app, name="run")


@app.command()
def status() -> None:
    """Show the current quest stage and next action."""
    print_status()


@run_app.command("skill")
def run_skill(
    skill_name: str,
    quest: Annotated[str, typer.Option("--quest")],
) -> None:
    """Run a BuildGuild skill for a quest."""
    if quest != "quest-01":
        raise typer.BadParameter("Only quest-01 is available in this POC.", param_hint="--quest")

    if skill_name == "test-baseline-rag":
        from buildguild.skills.test_baseline_rag import run

        run()
        return

    if skill_name == "maya-tests-outputs":
        from buildguild.skills.maya_tests_outputs import run

        run()
        return

    raise typer.BadParameter(
        "Unknown skill. Available skills: maya-tests-outputs, test-baseline-rag.",
        param_hint="skill_name",
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
