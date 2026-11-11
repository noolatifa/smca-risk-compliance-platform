from datetime import date, timedelta

API = "/api/v1"


def creer_activite(client, nom):
    response = client.post(
        f"{API}/activites",
        json={
            "nom": nom,
            "description": "Activité de test.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_risque(client, activite_id, probabilite, impact):
    response = client.post(
        f"{API}/risques",
        json={
            "scenario": f"Risque {probabilite}-{impact}",
            "cause": "Panne technique",
            "menace": "Défaillance serveur",
            "vulnerabilite": "Absence de redondance",
            "consequences": "Interruption du service",
            "proprietaire": "Responsable informatique",
            "activite_ids": [activite_id],
            "ressource_ids": [],
            "probabilite": probabilite,
            "impact": impact,
            "statut": "brouillon",
        },
    )

    assert response.status_code == 201

    risque = response.json()
    risque_id = risque["id"]

    response = client.post(
        f"{API}/risques/{risque_id}/soumettre"
    )
    assert response.status_code == 200

    response = client.post(
        f"{API}/risques/{risque_id}/valider"
    )
    assert response.status_code == 200

    return response.json()


def creer_traitement(client, risque_id, statut="planifie"):
    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": risque_id,
            "mesure": "Mettre en place une sauvegarde quotidienne",
            "responsable": "Responsable informatique",
            "echeance": str(
                date.today() + timedelta(days=10)
            ),
            "statut": statut,
            "description": "Sauvegarde automatique.",
            "commentaire": "Mesure prioritaire.",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_dashboard_vide(client):
    response = client.get(
        f"{API}/dashboard"
    )

    assert response.status_code == 200

    dashboard = response.json()

    assert dashboard["indicateurs"]["total_risques"] == 0
    assert dashboard["indicateurs"]["risques_faibles"] == 0
    assert dashboard["indicateurs"]["risques_moderees"] == 0
    assert dashboard["indicateurs"]["risques_eleves"] == 0
    assert dashboard["indicateurs"]["mesures_en_retard"] == 0

    assert dashboard["repartition_niveaux"] == {
        "faible": 0,
        "modere": 0,
        "eleve": 0,
    }

    assert dashboard["risques_par_activite"] == []
    assert dashboard["top_risques"] == []

    assert dashboard["suivi_traitements"] == {
        "planifies": 0,
        "en_cours": 0,
        "termines": 0,
        "annules": 0,
        "en_retard": 0,
    }


def test_dashboard_compte_les_risques_par_niveau(client):
    activite_faible = creer_activite(
        client,
        "Newsletter",
    )

    activite_modere = creer_activite(
        client,
        "Catalogue produits",
    )

    activite_eleve = creer_activite(
        client,
        "Paiement en ligne",
    )

    creer_risque(
        client,
        activite_faible["id"],
        1,
        2,
    )

    creer_risque(
        client,
        activite_modere["id"],
        2,
        4,
    )

    creer_risque(
        client,
        activite_eleve["id"],
        5,
        5,
    )

    response = client.get(
        f"{API}/dashboard"
    )

    assert response.status_code == 200

    dashboard = response.json()

    assert dashboard["indicateurs"]["total_risques"] == 3
    assert dashboard["indicateurs"]["risques_faibles"] == 1
    assert dashboard["indicateurs"]["risques_moderees"] == 1
    assert dashboard["indicateurs"]["risques_eleves"] == 1

    assert dashboard["repartition_niveaux"] == {
        "faible": 1,
        "modere": 1,
        "eleve": 1,
    }


def test_dashboard_exclut_les_risques_non_valides(client):
    activite = creer_activite(
        client,
        "Gestion des commandes",
    )

    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "Risque brouillon",
            "cause": "Cause",
            "menace": "Menace",
            "vulnerabilite": "Vulnerabilite",
            "consequences": "Consequences",
            "proprietaire": "Responsable",
            "activite_ids": [activite["id"]],
            "ressource_ids": [],
            "probabilite": 5,
            "impact": 5,
            "statut": "brouillon",
        },
    )

    assert response.status_code == 201

    dashboard = client.get(
        f"{API}/dashboard"
    )

    assert dashboard.status_code == 200
    assert dashboard.json()["indicateurs"]["total_risques"] == 0


def test_dashboard_retourne_les_risques_par_activite(client):
    activite_1 = creer_activite(
        client,
        "Paiement en ligne",
    )

    activite_2 = creer_activite(
        client,
        "Catalogue produits",
    )

    creer_risque(
        client,
        activite_1["id"],
        3,
        4,
    )

    creer_risque(
        client,
        activite_2["id"],
        4,
        4,
    )

    response = client.get(
        f"{API}/dashboard"
    )

    assert response.status_code == 200

    activites = response.json()[
        "risques_par_activite"
    ]

    assert len(activites) == 2

    noms = {
        activite["activite"]
        for activite in activites
    }

    assert noms == {
        "Paiement en ligne",
        "Catalogue produits",
    }

    for activite in activites:
        assert activite["nombre_risques"] == 1


def test_dashboard_retourne_top_trois_risques(client):
    activites = [
        creer_activite(client, "Activite 1"),
        creer_activite(client, "Activite 2"),
        creer_activite(client, "Activite 3"),
        creer_activite(client, "Activite 4"),
    ]

    creer_risque(
        client,
        activites[0]["id"],
        5,
        5,
    )

    creer_risque(
        client,
        activites[1]["id"],
        5,
        4,
    )

    creer_risque(
        client,
        activites[2]["id"],
        4,
        4,
    )

    creer_risque(
        client,
        activites[3]["id"],
        1,
        1,
    )

    response = client.get(
        f"{API}/dashboard"
    )

    assert response.status_code == 200

    top_risques = response.json()["top_risques"]

    assert len(top_risques) == 3
    assert top_risques[0]["score"] == 25
    assert top_risques[1]["score"] == 20
    assert top_risques[2]["score"] == 16


def test_dashboard_suivi_les_traitements(client):
    activites = [
        creer_activite(client, "Activite 1"),
        creer_activite(client, "Activite 2"),
        creer_activite(client, "Activite 3"),
        creer_activite(client, "Activite 4"),
    ]

    risques = [
        creer_risque(
            client,
            activites[0]["id"],
            5,
            5,
        ),
        creer_risque(
            client,
            activites[1]["id"],
            4,
            4,
        ),
        creer_risque(
            client,
            activites[2]["id"],
            3,
            3,
        ),
        creer_risque(
            client,
            activites[3]["id"],
            2,
            2,
        ),
    ]

    creer_traitement(
        client,
        risques[0]["id"],
        "planifie",
    )

    creer_traitement(
        client,
        risques[1]["id"],
        "en_cours",
    )

    traitement_termine = creer_traitement(
        client,
        risques[2]["id"],
        "planifie",
    )

    response = client.put(
        f"{API}/traitements/{traitement_termine['id']}",
        json={
            "statut": "termine",
            "date_realisation": str(date.today()),
        },
    )

    assert response.status_code == 200

    traitement_annule = creer_traitement(
        client,
        risques[3]["id"],
        "planifie",
    )

    response = client.put(
        f"{API}/traitements/{traitement_annule['id']}",
        json={
            "statut": "annule",
        },
    )

    assert response.status_code == 200

    dashboard = client.get(
        f"{API}/dashboard"
    )

    assert dashboard.status_code == 200

    suivi = dashboard.json()["suivi_traitements"]

    assert suivi["planifies"] == 1
    assert suivi["en_cours"] == 1
    assert suivi["termines"] == 1
    assert suivi["annules"] == 1
    assert suivi["en_retard"] == 0


def test_dashboard_detecte_les_mesures_en_retard(client):
    activite = creer_activite(
        client,
        "Paiement en ligne",
    )

    risque = creer_risque(
        client,
        activite["id"],
        5,
        5,
    )

    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": risque["id"],
            "mesure": "Mettre à jour le serveur",
            "responsable": "Administrateur",
            "echeance": str(
                date.today() - timedelta(days=3)
            ),
            "statut": "en_cours",
        },
    )

    assert response.status_code == 201

    dashboard = client.get(
        f"{API}/dashboard"
    )

    assert dashboard.status_code == 200

    resultat = dashboard.json()

    assert resultat["indicateurs"]["mesures_en_retard"] == 1
    assert resultat["suivi_traitements"]["en_retard"] == 1