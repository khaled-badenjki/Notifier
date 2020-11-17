from flask import url_for

from notifier.models import Group


def test_create_group(client, db, admin_headers):
    # test bad data
    groups_url = url_for('api.groups')
    data = {}
    rep = client.post(groups_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["name"] = "group1"

    rep = client.post(groups_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    group = db.session.query(Group).filter_by(id=data["group"]["id"]).first()

    assert group.name == "group1"


def test_get_all_group(client, db, group_factory, admin_headers):
    groups_url = url_for('api.groups')
    groups = group_factory.create_batch(30)

    db.session.add_all(groups)
    db.session.commit()

    rep = client.get(groups_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for group in groups:
        assert any(u["id"] == group.id for u in results["results"])
