import nox


@nox.session(python=["3.10"])
def test(session):
    session.install("poetry")
    session.run("poetry", "lock", "--no-update")
    session.run(
        "poetry",
        "install",
    )
    session.run("pytest", "app/tests")


@nox.session
def coverage(session):
    session.install("poetry")
    session.run("poetry", "lock", "--no-update")
    session.run("poetry", "install")
    session.run("pytest", "--cov-report=term-missing", "--cov=app", "app/tests")


@nox.session
def lint(session):
    session.install("poetry")
    session.run("poetry", "lock", "--no-update")
    session.run("poetry", "install")
    session.run("black", "./app")
    session.run("flake8")
    session.run("pytest", "--isort")


@nox.session
def typing(session):
    session.install("poetry")
    session.run("poetry", "lock", "--no-update")
    session.run("poetry", "install")
    session.run("pyright", "./app")
