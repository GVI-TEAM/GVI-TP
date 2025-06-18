"""
Tests d'intégration pour les routes API des salles.
"""

def test_create_salle_api(client):
    """Test de création d'une salle via API."""
    salle_data = {
        "nom": "Salle API Test",
        "capacite": 30,
        "localisation": "Bâtiment Test"
    }
    
    response = client.post("/api/v1/salles", json=salle_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == salle_data["nom"]
    assert data["capacite"] == salle_data["capacite"]
    assert data["localisation"] == salle_data["localisation"]
    assert "id" in data

def test_create_duplicate_salle_api(client):
    """Test de création d'une salle avec nom dupliqué."""
    salle_data = {
        "nom": "Salle Duplicate",
        "capacite": 25,
        "localisation": "Test"
    }
    
    # Première création
    response1 = client.post("/api/v1/salles", json=salle_data)
    assert response1.status_code == 201
    
    # Tentative de duplication
    response2 = client.post("/api/v1/salles", json=salle_data)
    assert response2.status_code == 400
    assert "Une salle avec ce nom existe déjà" in response2.json()["detail"]

def test_get_salles_api(client):
    """Test de récupération des salles via API."""
    # Créer quelques salles
    salles_data = [
        {"nom": "Salle 1", "capacite": 20, "localisation": "Test"},
        {"nom": "Salle 2", "capacite": 30, "localisation": "Test"}
    ]
    
    for salle_data in salles_data:
        client.post("/api/v1/salles", json=salle_data)
    
    # Récupérer toutes les salles
    response = client.get("/api/v1/salles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_salles_with_filter_api(client):
    """Test de récupération des salles."""
    # Créer des salles
    salles_data = [
        {"nom": "Salle 1", "capacite": 20, "localisation": "Test"},
        {"nom": "Salle 2", "capacite": 30, "localisation": "Test"}
    ]
    
    for salle_data in salles_data:
        client.post("/api/v1/salles", json=salle_data)
    
    # Récupérer toutes les salles
    response = client.get("/api/v1/salles")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert isinstance(data, list)

def test_get_salle_by_id_api(client):
    """Test de récupération d'une salle par ID."""
    # Créer une salle
    salle_data = {"nom": "Salle Get ID", "capacite": 25, "localisation": "Test"}
    response = client.post("/api/v1/salles", json=salle_data)
    created_salle = response.json()
    
    # Récupérer par ID
    response = client.get(f"/api/v1/salles/{created_salle['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_salle["id"]
    assert data["nom"] == salle_data["nom"]

def test_get_nonexistent_salle_api(client):
    """Test de récupération d'une salle inexistante."""
    response = client.get("/api/v1/salles/nonexistent-id")
    
    assert response.status_code == 404
    assert "Salle non trouvée" in response.json()["detail"]

def test_update_salle_api(client):
    """Test de mise à jour d'une salle."""
    # Créer une salle
    salle_data = {"nom": "Salle Update API", "capacite": 20, "localisation": "Test"}
    response = client.post("/api/v1/salles", json=salle_data)
    created_salle = response.json()
    
    # Mettre à jour
    update_data = {"nom": "Salle Modifiée", "capacite": 40}
    response = client.put(f"/api/v1/salles/{created_salle['id']}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Salle Modifiée"
    assert data["capacite"] == 40
    assert data["localisation"] == "Test"  # Non modifié

def test_delete_salle_api(client):
    """Test de suppression d'une salle."""
    # Créer une salle
    salle_data = {"nom": "Salle Delete API", "capacite": 20, "localisation": "Test"}
    response = client.post("/api/v1/salles", json=salle_data)
    created_salle = response.json()
    
    # Supprimer
    response = client.delete(f"/api/v1/salles/{created_salle['id']}")
    
    assert response.status_code == 204
    
    # Vérifier qu'elle n'existe plus
    response = client.get(f"/api/v1/salles/{created_salle['id']}")
    assert response.status_code == 404
