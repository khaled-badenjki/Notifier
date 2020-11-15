import click
from flask.cli import FlaskGroup

from notifier.app import create_app


def create_notifier(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_notifier)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user"""
    from notifier.extensions import db
    from notifier.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
