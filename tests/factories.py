import factory
from notifier.models import User, Customer, Group, Device


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


class CustomerFactory(factory.Factory):

    name = factory.Sequence(lambda n: "%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    phone = factory.Sequence(lambda n: '123-555-%04d' % n)

    class Meta:
        model = Customer


class GroupFactory(factory.Factory):
    name = factory.Sequence(lambda n: "%d" % n)

    class Meta:
        model = Group


class DeviceFactory(factory.Factory):
    registration_id = factory.Sequence(lambda n: '12as1213%04d' % n)
    customer_id = factory.Sequence(lambda n: '%04d' % n)
    type = factory.Iterator(["ios", "android"])
    version = factory.Sequence(lambda n: "Agent %03d" % n)

    class Meta:
        model = Device
