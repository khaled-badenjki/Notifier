from flask import url_for

from notifier.models import Customer


def test_put_customer(client, db, customer, admin_headers):
    # test 404
    customer_url = url_for('api.customer_by_id', customer_id="100000")
    rep = client.put(customer_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(customer)
    db.session.commit()

    data = {"name": "updated"}

    customer_url = url_for('api.customer_by_id', customer_id=customer.id)
    # test update customer
    rep = client.put(customer_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["customer"]
    assert data["name"] == "updated"
    assert data["email"] == customer.email
    assert data["phone"] == customer.phone
    assert data["language"] == customer.language


def test_delete_customer(client, db, customer, admin_headers):
    # test 404
    customer_url = url_for('api.customer_by_id', customer_id="100000")
    rep = client.delete(customer_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(customer)
    db.session.commit()

    # test get_customer

    customer_url = url_for('api.customer_by_id', customer_id=customer.id)
    rep = client.delete(customer_url,  headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(Customer).filter_by(id=customer.id).first() is None


def test_create_customer(client, db, admin_headers):
    # test bad data
    customers_url = url_for('api.customers')
    data = {"name": "created"}
    rep = client.post(customers_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["email"] = "create@mail.com"
    data["phone"] = "01111496284"
    data["language"] = "ar"

    rep = client.post(customers_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    customer = db.session.query(Customer).filter_by(id=data["customer"]["id"]).first()

    assert customer.name == "created"
    assert customer.email == "create@mail.com"
    assert customer.phone == "01111496284"
    assert customer.language == "ar"


def test_get_all_customer(client, db, customer_factory, admin_headers):
    customers_url = url_for('api.customers')
    customers = customer_factory.create_batch(30)

    db.session.add_all(customers)
    db.session.commit()

    rep = client.get(customers_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for customer in customers:
        assert any(u["id"] == customer.id for u in results["results"])
