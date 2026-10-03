def test_get_favorites(client):
    response = client.get("/api/favorites")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)

    for favorite in data:
        assert "id" in favorite
        assert "city" in favorite
        assert "country" in favorite
        assert "latitude" in favorite
        assert "longitude" in favorite


def test_add_favorite(client):
    favorite = {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }

    response = client.get("/api/favorites")

    assert response.status_code == 200
    assert response.get_json() == []

    response = client.post(
        "/api/favorites",
        json=favorite,
    )

    assert response.status_code == 201
    print(response.get_json())


def test_add_duplicate_favorite(client):
    favorite = {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }

    first_response = client.post(
        "/api/favorites",
        json=favorite,
    )

    assert first_response.status_code == 201

    first_data = first_response.get_json()

    second_response = client.post(
        "/api/favorites",
        json=favorite,
    )

    assert second_response.status_code == 200

    second_data = second_response.get_json()

    assert second_data["id"] == first_data["id"]
    assert second_data["city"] == "London"
    assert second_data["country"] == "United Kingdom"


def test_delete_favorite(client):
    favorite = {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }

    create_response = client.post(
        "/api/favorites",
        json=favorite,
    )

    assert create_response.status_code == 201

    favorite_id = create_response.get_json()["id"]

    delete_response = client.delete(
        f"/api/favorites/{favorite_id}"
    )

    assert delete_response.status_code == 200

    response = client.get("/api/favorites")

    assert response.status_code == 200
    assert response.get_json() == []


def test_delete_nonexistent_favorite(client):
    response = client.delete("/api/favorites/999")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Favorite not found"


def test_get_favorites_after_add(client):
    favorite = {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }

    create_response = client.post(
        "/api/favorites",
        json=favorite,
    )

    assert create_response.status_code == 201

    response = client.get("/api/favorites")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1

    assert data[0]["city"] == "London"
    assert data[0]["country"] == "United Kingdom"
    assert data[0]["latitude"] == 51.5074
    assert data[0]["longitude"] == -0.1278


def test_get_favorites_sorted(client):
    favorites = [
        {
            "city": "Tokyo",
            "country": "Japan",
            "latitude": 35.6762,
            "longitude": 139.6503,
        },
        {
            "city": "Berlin",
            "country": "Germany",
            "latitude": 52.5200,
            "longitude": 13.4050,
        },
        {
            "city": "London",
            "country": "United Kingdom",
            "latitude": 51.5074,
            "longitude": -0.1278,
        },
    ]

    for favorite in favorites:
        response = client.post(
            "/api/favorites",
            json=favorite,
        )

        assert response.status_code == 201

    response = client.get("/api/favorites")

    assert response.status_code == 200
    data = response.get_json()

    assert [favorite["city"] for favorite in data] == [
        "Berlin",
        "London",
        "Tokyo",
    ] 


def test_add_favorite_missing_fields(client):
    favorite = {
        "city": "London",
        "country": "United Kingdom",
    }

    response = client.post(
        "/api/favorites",
        json=favorite,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"


def test_add_favorite_empty_json(client):
    response = client.post(
        "/api/favorites",
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"
