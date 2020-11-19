import click
import random
from flask.cli import FlaskGroup
from notifier.models.device import Device
from notifier.app import create_app
from notifier.extensions import db
from notifier.models.customer import Customer, Group


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
    click.echo("dropping database..")
    db.drop_all()
    db.create_all()

    click.echo("creating groups..")
    for chunk in range(0, 1, 5):
        db.session.add_all(
            [
                Group(
                    name="group name %d" % i,
                )
                for i in range(chunk, chunk + 5)
            ]
        )
        db.session.flush()
    db.session.commit()
    click.echo("created 5 groups")

    click.echo("creating customers..")
    groups = Group.query.all()
    for chunk in range(0, 10, 100):
        db.session.add_all(
            [
                Customer(
                    name="customer name %d" % i,
                    email="customer%d@mail.com" % i,
                    phone="0111111111%d" % i,
                    language=random.choice(["ar", "en"]),
                    customer_groups=groups,
                )
                for i in range(chunk, chunk + 100)
            ]
        )
        db.session.flush()
    db.session.commit()
    click.echo("created 100 customers")

    click.echo("creating devices..")
    customers = Customer.query.all()
    for customer in customers:
        db.session.add_all(
            [
                Device(
                    customer_id=customer.id,
                    registration_id="123123123123%d" % customer.id,
                    type=random.choice(["android", "ios"]),
                    version="4.1.%d" % customer.id,
                )
            ]
        )
        db.session.flush()
    db.session.commit()
    click.echo("created customers devices")


if __name__ == "__main__":
    cli()
