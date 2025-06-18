"""
Tests d'intégration pour les routes API des réservations.
"""
def test_create_reservation_api(client):
    """Test de création d'une réservation via API."""
    # Créer une salle d'abord
    salle_data = {"nom": "Salle Réservation", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une réservation
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2024-12-25",
        "heure": "14:00:00",
        "utilisateur": "John Doe",
        "commentaire": "Réunion importante"
    }
    
    response = client.post("/api/v1/reservations", json=reservation_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["salle_id"] == salle["id"]
    assert data["date"] == "2024-12-25"
    assert data["heure"] == "14:00:00"
    assert data["utilisateur"] == "John Doe"
    assert "id" in data

def test_create_reservation_nonexistent_salle_api(client):
    """Test de création d'une réservation avec salle inexistante."""
    reservation_data = {
        "salle_id": "nonexistent-id",
        "date": "2024-12-25",
        "heure": "14:00:00",
        "utilisateur": "John Doe"
    }
    
    response = client.post("/api/v1/reservations", json=reservation_data)
    
    assert response.status_code == 404
    assert "Salle non trouvée" in response.json()["detail"]

def test_create_reservation_conflict_api(client):
    """Test de création d'une réservation en conflit."""
    # Créer une salle
    salle_data = {"nom": "Salle Conflit API", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une première réservation
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2024-12-25",
        "heure": "14:00:00",
        "utilisateur": "User 1"
    }
    response1 = client.post("/api/v1/reservations", json=reservation_data)
    assert response1.status_code == 201
    
    # Tenter de créer une réservation en conflit
    reservation_data_conflict = {
        "salle_id": salle["id"],
        "date": "2024-12-25",
        "heure": "14:00:00",  # Même heure
        "utilisateur": "User 2"
    }
    response2 = client.post("/api/v1/reservations", json=reservation_data_conflict)
    
    assert response2.status_code == 400
    assert "Cette salle est déjà réservée" in response2.json()["detail"]

def test_get_reservations_api(client):
    """Test de récupération des réservations via API."""
    # Créer une salle
    salle_data = {"nom": "Salle Get Reservations", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer des réservations
    reservations_data = [
        {
            "salle_id": salle["id"],
            "date": "2024-12-25",
            "heure": "10:00:00",
            "utilisateur": "User 1"
        },
        {
            "salle_id": salle["id"],
            "date": "2024-12-25",
            "heure": "14:00:00",
            "utilisateur": "User 2"
        }
    ]
    
    for reservation_data in reservations_data:
        client.post("/api/v1/reservations", json=reservation_data)
    
    # Récupérer toutes les réservations
    response = client.get("/api/v1/reservations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_reservations_by_salle_api(client):
    """Test de récupération des réservations par salle."""
    # Créer deux salles
    salle1_data = {"nom": "Salle 1 Reservations", "capacite": 20, "localisation": "Test"}
    salle2_data = {"nom": "Salle 2 Reservations", "capacite": 30, "localisation": "Test"}
    salle1_response = client.post("/api/v1/salles", json=salle1_data)
    salle2_response = client.post("/api/v1/salles", json=salle2_data)
    salle1 = salle1_response.json()
    salle2 = salle2_response.json()
    
    # Créer des réservations
    reservations_data = [
        {"salle_id": salle1["id"], "date": "2024-12-25", "heure": "10:00:00", "utilisateur": "User 1"},
        {"salle_id": salle1["id"], "date": "2024-12-25", "heure": "14:00:00", "utilisateur": "User 2"},
        {"salle_id": salle2["id"], "date": "2024-12-25", "heure": "10:00:00", "utilisateur": "User 3"}
    ]
    
    for reservation_data in reservations_data:
        client.post("/api/v1/reservations", json=reservation_data)
    
    # Récupérer les réservations par salle
    response1 = client.get(f"/api/v1/salles/{salle1['id']}/reservations")
    response2 = client.get(f"/api/v1/salles/{salle2['id']}/reservations")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    
    assert len(data1) == 2
    assert len(data2) == 1

def test_get_reservation_by_id_api(client):
    """Test de récupération d'une réservation par ID."""
    # Créer une salle
    salle_data = {"nom": "Salle Get Reservation ID", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une réservation
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2024-12-25",
        "heure": "14:00:00",
        "utilisateur": "John Doe"
    }
    response = client.post("/api/v1/reservations", json=reservation_data)
    created_reservation = response.json()
    
    # Récupérer par ID
    response = client.get(f"/api/v1/reservations/{created_reservation['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_reservation["id"]
    assert data["utilisateur"] == "John Doe"