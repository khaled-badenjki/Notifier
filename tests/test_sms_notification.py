from flask import url_for

from notifier.models import Notification


def test_create_sms_notification(client, db, admin_headers):
    # test bad data
    sms_notifications_url = url_for('api.sms_notifications')
    data = {"customer_id": 1}
    rep = client.post(sms_notifications_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["text"] = "hello there"

    rep = client.post(sms_notifications_url, json=data, headers=admin_headers)
    assert rep.status_code == 422

    # create customer to pass validation of customer exists
    customers_url = url_for('api.customers')
    customer_data = {"name": "created", "email": "created@mail.com", "phone": "01111111"}
    client.post(customers_url, json=customer_data, headers=admin_headers)

    rep = client.post(sms_notifications_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    notification = db.session.query(Notification).filter_by(id=data["notification"]["id"]).first()

    assert notification.customer_id == 1
    assert notification.text == "hello there"


def test_get_all_sms_notification(client, db, sms_notification_factory, admin_headers):
    sms_notifications_url = url_for('api.sms_notifications')
    sms_notifications = sms_notification_factory.create_batch(30)

    db.session.add_all(sms_notifications)
    db.session.commit()

    rep = client.get(sms_notifications_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for sms_notification in sms_notifications:
        assert any(u["id"] == sms_notification.id for u in results["results"])
