API = "/api/v1"


def creer_activite(client, nom):
    response = client.post(
        f"{API}/activites",
        json={
            "nom": nom,
            "description": "Activité de test",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_risque(client, activite_id, probabilite, impact):
    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "Risque de test",
            "cause": "Cause de test",
            "menace": "Menace de test",
            "vulnerabilite": "Vulnérabilité de test",
            "consequences": "Conséquences de test",
            "proprietaire": "Responsable de test",
            "activite_ids": [activite_id],
            "probabilite": probabilite,
            "impact": impact,
        },
    )

    assert response.status_code == 201

    risque = response.json()

    client.post(
        f"{API}/risques/{risque['id']}/soumettre"
    )

    validation = client.post(
        f"{API}/risques/{risque['id']}/valider"
    )

    assert validation.status_code == 200

    return risque


def test_heatmap_utilise_uniquement_les_risques_valides(client):
    activite = creer_activite(client, "Paiement")

    risque = creer_risque(
        client,
        activite["id"],
        5,
        5,
    )

    response = client.get(
        f"{API}/cartographie/heatmap"
    )

    assert response.status_code == 200

    resultat = response.json()

    assert resultat["total_risques"] == 1
    assert resultat["risques_eleves"] == 1
    assert resultat["risques"][0]["id"] == risque["id"]


def test_heatmap_5x5(client):
    activite = creer_activite(client, "Transfert")

    creer_risque(
        client,
        activite["id"],
        5,
        5,
    )

    response = client.get(
        f"{API}/cartographie/heatmap"
    )

    assert response.status_code == 200

    matrice = response.json()["matrice"]

    assert len(matrice) == 25


def test_statistiques_cartographie(client):
    activite_1 = creer_activite(client, "Paiement")
    activite_2 = creer_activite(client, "Change")
    activite_3 = creer_activite(client, "Portefeuille mobile")

    creer_risque(client, activite_1["id"], 1, 2)
    creer_risque(client, activite_2["id"], 2, 4)
    creer_risque(client, activite_3["id"], 4, 5)

    response = client.get(
        f"{API}/cartographie/statistiques"
    )

    assert response.status_code == 200

    statistiques = response.json()

    assert statistiques["total_risques"] == 3
    assert statistiques["risques_faibles"] == 1
    assert statistiques["risques_moderees"] == 1
    assert statistiques["risques_eleves"] == 1
    assert len(statistiques["top_risques"]) == 3


def test_cartographie_vide(client):
    response = client.get(
        f"{API}/cartographie"
    )

    assert response.status_code == 200

    resultat = response.json()

    assert resultat["total_risques"] == 0
    assert resultat["risques"] == []
    assert len(resultat["matrice"]) == 25