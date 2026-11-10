from datetime import date, timedelta

API = "/api/v1"


def creer_activite(client):
    response = client.post(
        f"{API}/activites",
        json={
            "nom": "Traiter un paiement",
            "description": "Activité critique.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_ressource(client):
    response = client.post(
        f"{API}/ressources",
        json={
            "nom": "Application de paiement",
            "type_ressource": "application",
            "description": "Application principale.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_risque_valide(client):
    activite = creer_activite(client)
    ressource = creer_ressource(client)

    risque = client.post(
        f"{API}/risques",
        json={
            "scenario": "Indisponibilité de l'application",
            "cause": "Panne serveur",
            "menace": "Défaillance technique",
            "vulnerabilite": "Absence de redondance",
            "consequences": "Interruption du paiement",
            "proprietaire": "Responsable informatique",
            "activite_ids": [activite["id"]],
            "ressource_ids": [ressource["id"]],
            "probabilite": 5,
            "impact": 5,
        },
    )

    assert risque.status_code == 201
    risque_id = risque.json()["id"]

    soumis = client.post(
        f"{API}/risques/{risque_id}/soumettre"
    )
    assert soumis.status_code == 200

    valide = client.post(
        f"{API}/risques/{risque_id}/valider"
    )
    assert valide.status_code == 200

    return valide.json()


def creer_traitement(client, echeance=None):
    risque = creer_risque_valide(client)

    if echeance is None:
        echeance = str(date.today() + timedelta(days=10))

    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": risque["id"],
            "mesure": "Mettre en place une sauvegarde quotidienne",
            "responsable": "Responsable informatique",
            "echeance": echeance,
            "statut": "planifie",
            "description": "Sauvegarde automatique des données.",
            "commentaire": "Mesure prioritaire.",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_creation_traitement(client):
    traitement = creer_traitement(client)

    assert traitement["risque_id"] > 0
    assert traitement["mesure"] == (
        "Mettre en place une sauvegarde quotidienne"
    )
    assert traitement["responsable"] == "Responsable informatique"
    assert traitement["statut"] == "planifie"
    assert traitement["en_retard"] is False


def test_obtenir_traitement(client):
    traitement = creer_traitement(client)

    response = client.get(
        f"{API}/traitements/{traitement['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == traitement["id"]


def test_lister_traitements(client):
    creer_traitement(client)
    creer_traitement(client)

    response = client.get(
        f"{API}/traitements"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_modifier_traitement(client):
    traitement = creer_traitement(client)

    response = client.put(
        f"{API}/traitements/{traitement['id']}",
        json={
            "mesure": "Mettre en place une réplication des données",
            "responsable": "Directeur informatique",
            "statut": "en_cours",
        },
    )

    assert response.status_code == 200

    resultat = response.json()

    assert resultat["mesure"] == (
        "Mettre en place une réplication des données"
    )
    assert resultat["responsable"] == "Directeur informatique"
    assert resultat["statut"] == "en_cours"


def test_traitement_termine_avec_date_realisation(client):
    traitement = creer_traitement(client)

    response = client.put(
        f"{API}/traitements/{traitement['id']}",
        json={
            "statut": "termine",
            "date_realisation": str(date.today()),
        },
    )

    assert response.status_code == 200

    resultat = response.json()

    assert resultat["statut"] == "termine"
    assert resultat["date_realisation"] == str(date.today())
    assert resultat["en_retard"] is False


def test_traitement_termine_sans_date_refuse(client):
    traitement = creer_traitement(client)

    response = client.put(
        f"{API}/traitements/{traitement['id']}",
        json={
            "statut": "termine",
        },
    )

    assert response.status_code == 422


def test_risque_non_valide_refuse(client):
    activite = creer_activite(client)

    risque = client.post(
        f"{API}/risques",
        json={
            "scenario": "Risque non validé",
            "cause": "Test",
            "menace": "Test",
            "vulnerabilite": "Test",
            "consequences": "Test",
            "proprietaire": "Responsable",
            "activite_ids": [activite["id"]],
            "probabilite": 3,
            "impact": 3,
        },
    )

    assert risque.status_code == 201

    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": risque.json()["id"],
            "mesure": "Mesure de test",
            "responsable": "Responsable",
            "echeance": str(date.today() + timedelta(days=5)),
        },
    )

    assert response.status_code == 409


def test_risque_inexistant_refuse(client):
    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": 9999,
            "mesure": "Mesure de test",
            "responsable": "Responsable",
            "echeance": str(date.today() + timedelta(days=5)),
        },
    )

    assert response.status_code == 404


def test_lister_uniquement_traitements_en_retard(client):
    traitement = creer_traitement(
        client,
        echeance=str(date.today() - timedelta(days=2)),
    )

    response = client.get(
        f"{API}/traitements?uniquement_en_retard=true"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == traitement["id"]
    assert response.json()[0]["en_retard"] is True


def test_dashboard_traitements(client):
    creer_traitement(client)

    response = client.get(
        f"{API}/traitements/dashboard"
    )

    assert response.status_code == 200

    dashboard = response.json()

    assert dashboard["total"] == 1
    assert dashboard["planifies"] == 1
    assert dashboard["en_cours"] == 0
    assert dashboard["termines"] == 0
    assert dashboard["annules"] == 0


def test_supprimer_traitement(client):
    traitement = creer_traitement(client)

    response = client.delete(
        f"{API}/traitements/{traitement['id']}"
    )

    assert response.status_code == 204

    verification = client.get(
        f"{API}/traitements/{traitement['id']}"
    )

    assert verification.status_code == 404