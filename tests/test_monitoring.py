def test_monitoring(client):
    # create user and some debts
    client.post("/api/auth/register", json={
        "first_name":"Mon",
        "last_name":"User",
        "email":"mon@example.com",
        "password":"monpass"
    })
    r = client.post("/api/auth/token", data={"username":"mon@example.com", "password":"monpass"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # add debts
    client.post("/api/debts/", json={"debt_type":"owed_to","person_name":"A","amount":50,"currency":"UZS"}, headers=headers)
    client.post("/api/debts/", json={"debt_type":"owed_by","person_name":"B","amount":20,"currency":"UZS"}, headers=headers)

    r = client.get("/api/monitoring/", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "summary" in data
    assert any(item["currency"] == "UZS" for item in data["summary"])
