API = "/api/v1"


def creer_activite(client, nom="Transfert national"):
    r = client.post(f"{API}/activites", json={"nom": nom})
    assert r.status_code == 201
    return r.json()


def creer_ressource(client, nom="Système central", type_ressource="application"):
    r = client.post(
        f"{API}/ressources", json={"nom": nom, "type_ressource": type_ressource}
    )
    assert r.status_code == 201
    return r.json()


def test_health(client):
    assert client.get("/health").json() == {"status": "healthy"}


def test_creation_et_lecture(client):
    a = creer_activite(client)
    assert a["archive"] is False
    assert client.get(f"{API}/activites/{a['id']}").json()["nom"] == "Transfert national"
    assert client.get(f"{API}/activites/9999").status_code == 404


def test_validation_des_entrees(client):
    assert client.post(f"{API}/activites", json={"nom": ""}).status_code == 422
    assert client.post(f"{API}/activites", json={"nom": "x", "foo": 1}).status_code == 422
    r = client.post(f"{API}/ressources", json={"nom": "x", "type_ressource": "inconnu"})
    assert r.status_code == 422


def test_ressource_partagee_par_cinq_activites_sans_doublon(client):
    """T01 : une ressource partagée, toutes ses activités retrouvées sans doublon."""
    res = creer_ressource(client)

    for i in range(5):
        a = creer_activite(client, f"Activité agence {i}")
        r = client.post(
            f"{API}/dependances",
            json={"activite_id": a["id"], "ressource_id": res["id"], "criticite": 3},
        )
        assert r.status_code == 201

    liens = client.get(f"{API}/dependances", params={"ressource_id": res["id"]}).json()
    assert len({lien["activite_id"] for lien in liens}) == 5


def test_dependance_en_double_refusee(client):
    a, r = creer_activite(client), creer_ressource(client)
    corps = {"activite_id": a["id"], "ressource_id": r["id"], "criticite": 2}

    assert client.post(f"{API}/dependances", json=corps).status_code == 201
    assert client.post(f"{API}/dependances", json=corps).status_code == 409


def test_criticite_hors_bornes(client):
    a, r = creer_activite(client), creer_ressource(client)

    for valeur in (0, 5):
        rep = client.post(
            f"{API}/dependances",
            json={"activite_id": a["id"], "ressource_id": r["id"], "criticite": valeur},
        )
        assert rep.status_code == 422


def test_archivage_au_lieu_de_suppression(client):
    a, r = creer_activite(client), creer_ressource(client)

    assert client.post(f"{API}/activites/{a['id']}/archiver").json()["archive"] is True

    # masquée par défaut, visible sur demande, toujours consultable
    assert client.get(f"{API}/activites").json() == []
    assert len(client.get(f"{API}/activites", params={"inclure_archives": True}).json()) == 1
    assert client.get(f"{API}/activites/{a['id']}").status_code == 200

    # et on ne peut plus la lier
    rep = client.post(
        f"{API}/dependances",
        json={"activite_id": a["id"], "ressource_id": r["id"], "criticite": 1},
    )
    assert rep.status_code == 422
