import click
import random
from flask.cli import FlaskGroup
from notifier.app import create_app
from notifier.extensions import db
from notifier.models.customer import Customer


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


@cli.command("seed")
def seed():
    click.echo("delete current customers")
    Customer.query.delete()
    click.echo("create customers")
    for chunk in range(0, 10, 100):
        db.session.add_all(
            [
                Customer(
                    name="customer name %d" % i,
                    email="customer%d@mail.com" % i,
                    phone="0111111111%d" % i,
                    language=random.choice(["ar", "en"]),
                )
                for i in range(chunk, chunk + 100)
            ]
        )
        db.session.flush()
    db.session.commit()
    click.echo("created 100 customers")


if __name__ == "__main__":
    cli()
