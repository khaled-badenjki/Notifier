from flask import url_for

from notifier.models import Device


def test_put_device(client, db, device, admin_headers):
    # test 404
    device_url = url_for('api.device_by_id', device_id="100000")
    rep = client.put(device_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(device)
    db.session.commit()

    data = {"registration_id": "asd123asd123", "customer_id": 1, "type": "android", "version": "4.1.1"}

    device_url = url_for('api.device_by_id', device_id=device.id)
    # test update device
    rep = client.put(device_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["device"]
    assert data["registration_id"] == "asd123asd123"
    assert data["customer_id"] == device.customer_id
    assert data["type"] == device.type
    assert data["version"] == device.version


def test_delete_device(client, db, device, admin_headers):
    # test 404
    device_url = url_for('api.device_by_id', device_id="100000")
    rep = client.delete(device_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(device)
    db.session.commit()

    # test get_device

    device_url = url_for('api.device_by_id', device_id=device.id)
    rep = client.delete(device_url,  headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(Device).filter_by(id=device.id).first() is None


def test_create_device(client, db, admin_headers):
    # test bad data
    devices_url = url_for('api.devices')
    data = {"customer_id": 1, "type": "ios", "registration_id": "asd123"}
    rep = client.post(devices_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["version"] = "4.1.1"

    rep = client.post(devices_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    device = db.session.query(Device).filter_by(id=data["device"]["id"]).first()

    assert device.customer_id == 1
    assert device.registration_id == "asd123"
    assert device.type == "ios"
    assert device.version == "4.1.1"


def test_get_all_device(client, db, device_factory, admin_headers):
    devices_url = url_for('api.devices')
    devices = device_factory.create_batch(30)

    db.session.add_all(devices)
    db.session.commit()

    rep = client.get(devices_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for device in devices:
        assert any(u["id"] == device.id for u in results["results"])
