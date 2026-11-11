API = "/api/v1"


def creer_activite(client):
    response = client.post(
        f"{API}/activites",
        json={
            "nom": "Réaliser un transfert national",
            "description": "Activité critique de transfert.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_bia_complete(client):
    activite = creer_activite(client)

    response = client.post(
        f"{API}/bia",
        json={
            "activite_id": activite["id"],
            "responsable": "Responsable opérations",
            "heures_fonctionnement": "08:00-18:00",
            "sites_concernes": "Agence Tunis",
            "periode_pointe": "Fin de mois",
            "mtpd_heures": 8,
            "justification_mtpd": "Seuil maximal acceptable.",
            "rto_heures": 4,
            "capacite_minimale_pct": 50,
            "rpo_heures": 1,
            "justification_rpo": "Données récupérables.",
            "statut": "brouillon",
            "impacts": [
                {
                    "horizon_heures": 1,
                    "clients": "Impact limité.",
                    "operations": "Activité ralentie.",
                    "finances": "Impact faible.",
                    "engagements": "Engagements respectés.",
                    "reputation": "Pas d'impact majeur.",
                }
            ],
        },
    )

    assert response.status_code == 201
    return response.json()


def test_creation_bia_complete(client):
    bia = creer_bia_complete(client)

    assert bia["activite_id"] is not None
    assert bia["mtpd_heures"] == 8
    assert bia["rto_heures"] == 4
    assert bia["statut"] == "brouillon"
    assert len(bia["impacts"]) == 1


def test_modification_bia(client):
    bia = creer_bia_complete(client)

    modification = client.put(
        f"{API}/bia/{bia['id']}",
        json={
            "responsable": "Nouveau responsable",
            "rto_heures": 2,
            "capacite_minimale_pct": 70,
        },
    )

    assert modification.status_code == 200

    resultat = modification.json()

    assert resultat["responsable"] == "Nouveau responsable"
    assert resultat["rto_heures"] == 2
    assert resultat["capacite_minimale_pct"] == 70


def test_lister_bias(client):
    creer_bia_complete(client)

    response = client.get(
        f"{API}/bia"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_obtenir_bia(client):
    bia = creer_bia_complete(client)

    response = client.get(
        f"{API}/bia/{bia['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == bia["id"]


def test_workflow_validation_bia(client):
    bia = creer_bia_complete(client)

    soumission = client.post(
        f"{API}/bia/{bia['id']}/soumettre"
    )

    assert soumission.status_code == 200
    assert soumission.json()["statut"] == "soumis"

    validation = client.post(
        f"{API}/bia/{bia['id']}/valider"
    )

    assert validation.status_code == 200
    assert validation.json()["statut"] == "valide"