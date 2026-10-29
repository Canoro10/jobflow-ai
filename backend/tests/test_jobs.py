def test_create_job(client):
    response = client.post(
        "/jobs/",
        json={
            "company": "OpenAI",
            "position": "Python Backend Developer",
            "description": "Python FastAPI PostgreSQL",
            "remote": True,
            "salary": 2000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["company"] == "OpenAI"
    assert data["position"] == "Python Backend Developer"


def test_get_jobs(client):
    client.post(
        "/jobs/",
        json={
            "company": "Example Tech",
            "position": "Junior Python Developer",
            "description": "Python FastAPI",
            "remote": True,
            "salary": 1800,
        },
    )

    response = client.get("/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Example Tech"


def test_get_missing_job_returns_404(client):
    response = client.get("/jobs/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }


def test_update_job(client):
    created = client.post(
        "/jobs/",
        json={
            "company": "Acme",
            "position": "Python Developer",
            "description": "FastAPI",
            "remote": True,
            "salary": 1500,
        },
    )

    job_id = created.json()["id"]

    response = client.patch(
        f"/jobs/{job_id}",
        json={
            "salary": 2500,
        },
    )

    assert response.status_code == 200
    assert response.json()["salary"] == 2500
    assert response.json()["company"] == "Acme"


def test_delete_job(client):
    created = client.post(
        "/jobs/",
        json={
            "company": "Example",
            "position": "Backend Developer",
            "description": "Python",
            "remote": False,
            "salary": 1200,
        },
    )

    job_id = created.json()["id"]

    response = client.delete(f"/jobs/{job_id}")

    assert response.status_code == 204

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 404