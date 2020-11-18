from notifier.api.resources.user import UserResource, UserList
from notifier.api.resources.customer import CustomerResource, CustomerList
from notifier.api.resources.group import GroupResource, GroupList
from notifier.api.resources.device import DeviceResource, DeviceList
from notifier.api.resources.sms_notification import (
    SmsNotificationResource,
    SmsNotificationList,
)

__all__ = [
    "UserResource",
    "UserList",
    "CustomerResource",
    "CustomerList",
    "GroupResource",
    "GroupList",
    "DeviceResource",
    "DeviceList",
    "SmsNotificationResource",
    "SmsNotificationList",
]
