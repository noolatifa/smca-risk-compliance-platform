API = "/api/v1"


def creer_activite(client):
    response = client.post(
        f"{API}/activites",
        json={
            "nom": "Traiter un transfert",
            "description": "Activité critique.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_ressource(client):
    response = client.post(
        f"{API}/ressources",
        json={
            "nom": "Application transactionnelle",
            "type_ressource": "application",
            "description": "Système central.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_risque(client):
    activite = creer_activite(client)
    ressource = creer_ressource(client)

    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "Indisponibilité de l'application transactionnelle",
            "cause": "Panne du serveur applicatif",
            "menace": "Panne technique",
            "vulnerabilite": "Absence de basculement automatique",
            "consequences": "Interruption des transferts",
            "proprietaire": "Responsable informatique",
            "activite_ids": [activite["id"]],
            "ressource_ids": [ressource["id"]],
            "probabilite": 3,
            "impact": 4,
            "statut": "brouillon",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_creation_risque_et_calcul_criticite(client):
    risque = creer_risque(client)

    assert risque["probabilite"] == 3
    assert risque["impact"] == 4
    assert risque["score_criticite"] == 12
    assert risque["niveau"] == "eleve"
    assert risque["statut"] == "brouillon"


def test_lister_et_obtenir_risque(client):
    risque = creer_risque(client)

    liste = client.get(f"{API}/risques")

    assert liste.status_code == 200
    assert len(liste.json()) == 1

    detail = client.get(
        f"{API}/risques/{risque['id']}"
    )

    assert detail.status_code == 200
    assert detail.json()["id"] == risque["id"]


def test_modifier_risque(client):
    risque = creer_risque(client)

    response = client.put(
        f"{API}/risques/{risque['id']}",
        json={
            "probabilite": 2,
            "impact": 2,
            "proprietaire": "Nouveau responsable",
        },
    )

    assert response.status_code == 200

    resultat = response.json()

    assert resultat["probabilite"] == 2
    assert resultat["impact"] == 2
    assert resultat["score_criticite"] == 4
    assert resultat["niveau"] == "modere"
    assert resultat["proprietaire"] == "Nouveau responsable"


def test_workflow_risque(client):
    risque = creer_risque(client)

    soumission = client.post(
        f"{API}/risques/{risque['id']}/soumettre"
    )

    assert soumission.status_code == 200
    assert soumission.json()["statut"] == "soumis"

    validation = client.post(
        f"{API}/risques/{risque['id']}/valider"
    )

    assert validation.status_code == 200
    assert validation.json()["statut"] == "valide"


def test_probabilite_invalide(client):
    activite = creer_activite(client)

    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "Test",
            "cause": "Test",
            "menace": "Test",
            "vulnerabilite": "Test",
            "consequences": "Test",
            "proprietaire": "Test",
            "activite_ids": [activite["id"]],
            "ressource_ids": [],
            "probabilite": 5,
            "impact": 2,
        },
    )

    assert response.status_code == 422