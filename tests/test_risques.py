import pytest

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
        },
    )

    assert response.status_code == 201
    return response.json()


def test_creation_risque_et_calcul_criticite(client):
    risque = creer_risque(client)

    assert risque["probabilite"] == 3
    assert risque["impact"] == 4
    assert risque["score_criticite"] == 12
    assert risque["niveau"] == "modere"
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
    assert resultat["niveau"] == "faible"
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
            "probabilite": 6,
            "impact": 2,
        },
    )

    assert response.status_code == 422


def test_creation_directement_valide_refusee(client):
    activite = creer_activite(client)

    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "Test", "cause": "Test", "menace": "Test",
            "vulnerabilite": "Test", "consequences": "Test",
            "proprietaire": "Test", "activite_ids": [activite["id"]],
            "probabilite": 2, "impact": 2, "statut": "valide",
        },
    )

    assert response.status_code == 422


def test_risque_valide_non_modifiable(client):
    risque = creer_risque(client)
    client.post(f"{API}/risques/{risque['id']}/soumettre")
    client.post(f"{API}/risques/{risque['id']}/valider")

    response = client.put(
        f"{API}/risques/{risque['id']}",
        json={"probabilite": 1, "impact": 1},
    )

    assert response.status_code == 409


def test_grille_5x5_niveaux(client):
    # Grille 5x5 : 1-7 faible, 8-14 modéré, 15-25 élevé
    cas = [(1, 3, 3, "faible"), (2, 3, 6, "faible"), (2, 4, 8, "modere"),
           (3, 4, 12, "modere"), (3, 5, 15, "eleve"), (5, 5, 25, "eleve")]
    for p, i, score, niveau in cas:
        activite = creer_activite(client)
        r = client.post(f"{API}/risques", json={
            "scenario": "s", "cause": "c", "menace": "m", "vulnerabilite": "v",
            "consequences": "q", "proprietaire": "p",
            "activite_ids": [activite["id"]], "probabilite": p, "impact": i,
        }).json()
        assert (r["score_criticite"], r["niveau"]) == (score, niveau)



@pytest.mark.parametrize("probabilite, impact", [(0, 3), (6, 3), (3, 0), (3, 6)])
def test_notes_hors_echelle_refusees(client, probabilite, impact):
    activite = creer_activite(client)

    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "s", "cause": "c", "menace": "m", "vulnerabilite": "v",
            "consequences": "q", "proprietaire": "p",
            "activite_ids": [activite["id"]],
            "probabilite": probabilite, "impact": impact,
        },
    )

    assert response.status_code == 422