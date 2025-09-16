from datetime import datetime, timedelta

def get_auth_header(client):
    # ensure user exists
    client.post("/api/auth/register", json={
        "first_name":"Debt",
        "last_name":"User",
        "email":"debtuser@example.com",
        "password":"pass123"
    })
    r = client.post("/api/auth/token", data={"username":"debtuser@example.com", "password":"pass123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_crud_debt_and_filter(client):
    headers = get_auth_header(client)
    now = datetime.utcnow().isoformat()
    later = (datetime.utcnow() + timedelta(days=7)).isoformat()

    payload = {
        "debt_type": "owed_to",
        "person_name": "Ali",
        "amount": 100,
        "currency": "USD",
        "description": "Test debt",
        "start_date": now,
        "due_date": later
    }

    # create
    r = client.post("/api/debts/", json=payload, headers=headers)
    assert r.status_code == 201
    d = r.json()
    assert d["person_name"] == "Ali"

    debt_id = d["id"]

    # list all
    r = client.get("/api/debts/", headers=headers)
    assert r.status_code == 200
    assert any(x["id"] == debt_id for x in r.json())

    # filter by owed_to
    r = client.get("/api/debts/?debt_type=owed_to", headers=headers)
    assert r.status_code == 200
    assert all(x["debt_type"] == "owed_to" for x in r.json())

    # update
    payload["amount"] = 150
    r = client.put(f"/api/debts/{debt_id}", json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json()["amount"] == 150

    # delete
    r = client.delete(f"/api/debts/{debt_id}", headers=headers)
    assert r.status_code == 204
