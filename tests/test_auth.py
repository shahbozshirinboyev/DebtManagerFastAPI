def test_register_and_token(client):
    # register
    resp = client.post("/api/auth/register", json={
        "first_name":"Test",
        "last_name":"User",
        "email":"test@example.com",
        "password":"strongpass"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"

    # get token
    resp = client.post("/api/auth/token", data={"username":"test@example.com", "password":"strongpass"})
    assert resp.status_code == 200
    tok = resp.json()
    assert "access_token" in tok
