from datetime import date, timedelta


API = "/api/v1"


def creer_activite(client, nom="Paiement en ligne"):
    response = client.post(
        f"{API}/activites",
        json={
            "nom": nom,
            "description": "Activité de test.",
        },
    )

    assert response.status_code == 201
    return response.json()


def creer_risque(
    client,
    activite_id,
    statut="brouillon",
):
    response = client.post(
        f"{API}/risques",
        json={
            "scenario": "Indisponibilité du service",
            "cause": "Panne technique",
            "menace": "Défaillance serveur",
            "vulnerabilite": "Absence de redondance",
            "consequences": "Interruption du service",
            "proprietaire": "Responsable informatique",
            "activite_ids": [activite_id],
            "ressource_ids": [],
            "probabilite": 5,
            "impact": 5,
            "statut": statut,
        },
    )

    return response


def valider_risque(client, risque_id):
    response = client.post(
        f"{API}/risques/{risque_id}/soumettre"
    )

    assert response.status_code == 200

    response = client.post(
        f"{API}/risques/{risque_id}/valider"
    )

    assert response.status_code == 200


def test_export_risques_csv(client):
    activite = creer_activite(client)

    response = creer_risque(
        client,
        activite["id"],
    )

    assert response.status_code == 201

    risque = response.json()

    valider_risque(
        client,
        risque["id"],
    )

    response = client.get(
        f"{API}/exports/risques.csv"
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]

    contenu = response.content.decode(
        "utf-8-sig"
    )

    assert "ID" in contenu
    assert "Scénario" in contenu
    assert "Probabilité" in contenu
    assert "Impact" in contenu
    assert "Score" in contenu
    assert "Indisponibilité du service" in contenu
    assert "25" in contenu
    assert "eleve" in contenu


def test_export_risques_csv_exclut_brouillons(client):
    activite = creer_activite(client)

    response = creer_risque(
        client,
        activite["id"],
        statut="brouillon",
    )

    assert response.status_code == 201

    response = client.get(
        f"{API}/exports/risques.csv"
    )

    assert response.status_code == 200

    contenu = response.content.decode(
        "utf-8-sig"
    )

    assert "ID" in contenu
    assert "Indisponibilité du service" not in contenu


def test_export_traitements_csv(client):
    activite = creer_activite(client)

    response = creer_risque(
        client,
        activite["id"],
    )

    assert response.status_code == 201

    risque = response.json()

    valider_risque(
        client,
        risque["id"],
    )

    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": risque["id"],
            "mesure": "Mettre en place une sauvegarde",
            "responsable": "Responsable informatique",
            "echeance": str(
                date.today() + timedelta(days=10)
            ),
            "statut": "planifie",
            "description": "Sauvegarde automatique.",
            "commentaire": "Mesure prioritaire.",
        },
    )

    assert response.status_code == 201

    response = client.get(
        f"{API}/exports/traitements.csv"
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]

    contenu = response.content.decode(
        "utf-8-sig"
    )

    assert "Risque ID" in contenu
    assert "Mesure" in contenu
    assert "Responsable" in contenu
    assert "Échéance" in contenu
    assert "Mettre en place une sauvegarde" in contenu
    assert "Responsable informatique" in contenu
    
    
    
    
    
def test_export_risques_pdf(client):
    activite = creer_activite(
        client,
        "Paiement en ligne",
    )

    response = creer_risque(
        client,
        activite["id"],
    )

    assert response.status_code == 201

    risque = response.json()

    valider_risque(
        client,
        risque["id"],
    )

    response = client.get(
        f"{API}/exports/risques.pdf"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/pdf"
    )
    assert "attachment" in response.headers[
        "content-disposition"
    ]
    assert response.content.startswith(b"%PDF")


def test_export_traitements_pdf(client):
    activite = creer_activite(
        client,
        "Catalogue produits",
    )

    response = creer_risque(
        client,
        activite["id"],
    )

    assert response.status_code == 201

    risque = response.json()

    valider_risque(
        client,
        risque["id"],
    )

    response = client.post(
        f"{API}/traitements",
        json={
            "risque_id": risque["id"],
            "mesure": "Mettre en place une sauvegarde",
            "responsable": "Responsable informatique",
            "echeance": "2030-12-31",
            "statut": "planifie",
            "description": "Sauvegarde automatique.",
            "commentaire": "Mesure prioritaire.",
        },
    )

    assert response.status_code == 201

    response = client.get(
        f"{API}/exports/traitements.pdf"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/pdf"
    )
    assert "attachment" in response.headers[
        "content-disposition"
    ]
    assert response.content.startswith(b"%PDF")
    
    
    
    
def test_export_dashboard_pdf(client):
    response = client.get(
        f"{API}/exports/dashboard.pdf"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/pdf"
    )
    assert "attachment" in response.headers[
        "content-disposition"
    ]
    assert response.content.startswith(b"%PDF")