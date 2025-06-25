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

# v1.1.0 Tests for new features

def test_create_reservation_with_commentaire_api(client):
    """Test de création d'une réservation avec commentaire - v1.1.0."""
    # Créer une salle d'abord
    salle_data = {"nom": "Salle Commentaire", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une réservation avec commentaire
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2025-06-25",
        "heure": "14:00:00",
        "utilisateur": "John Doe",
        "commentaire": "Réunion équipe développement v1.1.0"
    }
    
    response = client.post("/api/v1/reservations", json=reservation_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["commentaire"] == "Réunion équipe développement v1.1.0"

def test_create_reservation_without_commentaire_api(client):
    """Test de création d'une réservation sans commentaire - v1.1.0."""
    # Créer une salle d'abord
    salle_data = {"nom": "Salle Sans Commentaire", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une réservation sans commentaire
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2025-06-26",
        "heure": "10:00:00",
        "utilisateur": "Jane Smith"
    }
    
    response = client.post("/api/v1/reservations", json=reservation_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["commentaire"] is None

def test_update_reservation_commentaire_api(client):
    """Test de mise à jour du commentaire d'une réservation - v1.1.0."""
    # Créer une salle
    salle_data = {"nom": "Salle Update Commentaire", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une réservation sans commentaire
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2025-06-27",
        "heure": "09:00:00",
        "utilisateur": "Bob Wilson"
    }
    response = client.post("/api/v1/reservations", json=reservation_data)
    created_reservation = response.json()
    
    # Mettre à jour avec un commentaire
    update_data = {"commentaire": "Mise à jour avec commentaire"}
    response = client.put(f"/api/v1/reservations/{created_reservation['id']}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["commentaire"] == "Mise à jour avec commentaire"

def test_delete_reservation_api(client):
    """Test de suppression d'une réservation - v1.1.0."""
    # Créer une salle
    salle_data = {"nom": "Salle Delete", "capacite": 20, "localisation": "Test"}
    salle_response = client.post("/api/v1/salles", json=salle_data)
    salle = salle_response.json()
    
    # Créer une réservation
    reservation_data = {
        "salle_id": salle["id"],
        "date": "2025-06-28",
        "heure": "15:00:00",
        "utilisateur": "Alice Brown",
        "commentaire": "Réservation à supprimer"
    }
    response = client.post("/api/v1/reservations", json=reservation_data)
    created_reservation = response.json()
    
    # Supprimer la réservation
    response = client.delete(f"/api/v1/reservations/{created_reservation['id']}")
    
    assert response.status_code == 204
    
    # Vérifier que la réservation n'existe plus
    response = client.get(f"/api/v1/reservations/{created_reservation['id']}")
    assert response.status_code == 404

def test_delete_nonexistent_reservation_api(client):
    """Test de suppression d'une réservation inexistante - v1.1.0."""
    response = client.delete("/api/v1/reservations/nonexistent-id")
    
    assert response.status_code == 404
    assert "Réservation non trouvée" in response.json()["detail"]