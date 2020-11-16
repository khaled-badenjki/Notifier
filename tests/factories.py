import factory
from notifier.models import User, Customer


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