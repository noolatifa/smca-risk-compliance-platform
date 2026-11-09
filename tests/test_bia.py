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


def test_creation_bia_complete(client):
    activite = creer_activite(client)

    response = client.post(
        f"{API}/bia",
        json={
            "activite_id": activite["id"],
            "responsable": "Responsable opérations",
            "heures_fonctionnement": "08:00-18:00",
            "sites_concernes": "Agences Tunis et Ariana",
            "periode_pointe": "Fin de mois",
            "mtpd_heures": 8,
            "justification_mtpd": "Au-delà de 8 heures, les impacts deviennent inacceptables.",
            "rto_heures": 4,
            "capacite_minimale_pct": 50,
            "rpo_heures": 1,
            "justification_rpo": "Les transactions confirmées doivent être récupérables.",
            "statut": "brouillon",
            "impacts": [
                {
                    "horizon_heures": 1,
                    "clients": "Retard limité pour les clients.",
                    "operations": "Fonctionnement dégradé.",
                    "finances": "Impact financier faible.",
                    "engagements": "Engagements encore respectés.",
                    "reputation": "Pas d'impact majeur.",
                }
            ],
        },
    )

    assert response.status_code == 201

    resultat = response.json()

    assert resultat["activite_id"] == activite["id"]
    assert resultat["mtpd_heures"] == 8
    assert resultat["rto_heures"] == 4
    assert resultat["statut"] == "brouillon"
    assert len(resultat["impacts"]) == 1