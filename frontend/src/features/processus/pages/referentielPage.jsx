import { useEffect, useState } from "react";

import {
  archiverActivite,
  archiverRessource,
  creerActivite,
  creerDependance,
  creerRessource,
  listerActivites,
  listerDependances,
  listerRessources,
} from "../services/referentielService";

import "./ReferentielPage.css";

function ReferentielPage() {
  const [onglet, setOnglet] = useState("activites");

  const [activites, setActivites] = useState([]);
  const [ressources, setRessources] = useState([]);
  const [dependances, setDependances] = useState([]);

  const [inclureArchives, setInclureArchives] = useState(false);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState("");
  const [message, setMessage] = useState("");

  const [activiteForm, setActiviteForm] = useState({
    nom: "",
    description: "",
  });

  const [ressourceForm, setRessourceForm] = useState({
    nom: "",
    type_ressource: "application",
    description: "",
  });

  const [dependanceForm, setDependanceForm] = useState({
    activite_id: "",
    ressource_id: "",
    type_dependance: "utilise",
  });

  async function chargerDonnees() {
    try {
      setChargement(true);
      setErreur("");

      const [activitesData, ressourcesData, dependancesData] =
        await Promise.all([
          listerActivites(inclureArchives),
          listerRessources(inclureArchives),
          listerDependances(),
        ]);

      setActivites(activitesData);
      setRessources(ressourcesData);
      setDependances(dependancesData);
    } catch (err) {
      setErreur(err.message);
    } finally {
      setChargement(false);
    }
  }

  useEffect(() => {
    chargerDonnees();
  }, [inclureArchives]);

  function modifierActiviteForm(event) {
    const { name, value } = event.target;

    setActiviteForm((ancienFormulaire) => ({
      ...ancienFormulaire,
      [name]: value,
    }));
  }

  function modifierRessourceForm(event) {
    const { name, value } = event.target;

    setRessourceForm((ancienFormulaire) => ({
      ...ancienFormulaire,
      [name]: value,
    }));
  }

  function modifierDependanceForm(event) {
    const { name, value } = event.target;

    setDependanceForm((ancienFormulaire) => ({
      ...ancienFormulaire,
      [name]: value,
    }));
  }

  async function soumettreActivite(event) {
    event.preventDefault();

    try {
      setErreur("");
      setMessage("");

      await creerActivite(activiteForm);

      setActiviteForm({
        nom: "",
        description: "",
      });

      setMessage("Activité créée avec succès.");
      await chargerDonnees();
    } catch (err) {
      setErreur(err.message);
    }
  }

  async function soumettreRessource(event) {
    event.preventDefault();

    try {
      setErreur("");
      setMessage("");

      await creerRessource(ressourceForm);

      setRessourceForm({
        nom: "",
        type_ressource: "application",
        description: "",
      });

      setMessage("Ressource créée avec succès.");
      await chargerDonnees();
    } catch (err) {
      setErreur(err.message);
    }
  }

  async function soumettreDependance(event) {
    event.preventDefault();

    try {
      setErreur("");
      setMessage("");

      await creerDependance({
        activite_id: Number(dependanceForm.activite_id),
        ressource_id: Number(dependanceForm.ressource_id),
        type_dependance: dependanceForm.type_dependance,
      });

      setDependanceForm({
        activite_id: "",
        ressource_id: "",
        type_dependance: "utilise",
      });

      setMessage("Dépendance créée avec succès.");
      await chargerDonnees();
    } catch (err) {
      setErreur(err.message);
    }
  }

  async function traiterArchivageActivite(id) {
    const confirmer = window.confirm(
      "Voulez-vous vraiment archiver cette activité ?",
    );

    if (!confirmer) {
      return;
    }

    try {
      setErreur("");
      setMessage("");

      await archiverActivite(id);

      setMessage("Activité archivée avec succès.");
      await chargerDonnees();
    } catch (err) {
      setErreur(err.message);
    }
  }

  async function traiterArchivageRessource(id) {
    const confirmer = window.confirm(
      "Voulez-vous vraiment archiver cette ressource ?",
    );

    if (!confirmer) {
      return;
    }

    try {
      setErreur("");
      setMessage("");

      await archiverRessource(id);

      setMessage("Ressource archivée avec succès.");
      await chargerDonnees();
    } catch (err) {
      setErreur(err.message);
    }
  }

  if (chargement) {
    return (
      <div className="referentiel-page-state">
        Chargement du référentiel...
      </div>
    );
  }

  return (
    <section className="referentiel-page">
      <header className="referentiel-header">
        <div>
          <p className="referentiel-kicker">GOUVERNANCE DU SI</p>
          <h2>Référentiel</h2>
          <p>
            Gérez les activités, les ressources et leurs dépendances.
          </p>
        </div>

        <label className="archive-switch">
          <input
            type="checkbox"
            checked={inclureArchives}
            onChange={(event) => setInclureArchives(event.target.checked)}
          />
          <span>Afficher les éléments archivés</span>
        </label>
      </header>

      {erreur && <div className="referentiel-alert error">{erreur}</div>}

      {message && (
        <div className="referentiel-alert success">{message}</div>
      )}

      <nav className="referentiel-tabs">
        <button
          className={onglet === "activites" ? "active" : ""}
          onClick={() => setOnglet("activites")}
        >
          Activités
          <span>{activites.length}</span>
        </button>

        <button
          className={onglet === "ressources" ? "active" : ""}
          onClick={() => setOnglet("ressources")}
        >
          Ressources
          <span>{ressources.length}</span>
        </button>

        <button
          className={onglet === "dependances" ? "active" : ""}
          onClick={() => setOnglet("dependances")}
        >
          Dépendances
          <span>{dependances.length}</span>
        </button>
      </nav>

      {onglet === "activites" && (
        <div className="referentiel-content">
          <article className="referentiel-form-card">
            <div className="card-heading">
              <p className="referentiel-kicker">NOUVEL ÉLÉMENT</p>
              <h3>Créer une activité</h3>
            </div>

            <form onSubmit={soumettreActivite}>
              <label>
                Nom
                <input
                  name="nom"
                  value={activiteForm.nom}
                  onChange={modifierActiviteForm}
                  placeholder="Ex. Traiter un transfert"
                  required
                />
              </label>

              <label>
                Description
                <textarea
                  name="description"
                  value={activiteForm.description}
                  onChange={modifierActiviteForm}
                  placeholder="Décrivez l'activité..."
                />
              </label>

              <button className="primary-button" type="submit">
                Créer l'activité
              </button>
            </form>
          </article>

          <article className="referentiel-table-card">
            <div className="card-heading">
              <p className="referentiel-kicker">RÉFÉRENTIEL MÉTIER</p>
              <h3>Activités enregistrées</h3>
            </div>

            {activites.length === 0 ? (
              <div className="empty-referentiel">
                Aucune activité enregistrée.
              </div>
            ) : (
              <div className="referentiel-table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nom</th>
                      <th>Description</th>
                      <th>Statut</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    {activites.map((activite) => (
                      <tr key={activite.id}>
                        <td>#{activite.id}</td>
                        <td className="strong-cell">{activite.nom}</td>
                        <td>{activite.description || "—"}</td>
                        <td>
                          <span
                            className={
                              activite.archive
                                ? "status-badge archived"
                                : "status-badge active-status"
                            }
                          >
                            {activite.archive ? "Archivée" : "Active"}
                          </span>
                        </td>
                        <td>
                          {!activite.archive && (
                            <button
                              className="table-action"
                              onClick={() =>
                                traiterArchivageActivite(activite.id)
                              }
                            >
                              Archiver
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </article>
        </div>
      )}

      {onglet === "ressources" && (
        <div className="referentiel-content">
          <article className="referentiel-form-card">
            <div className="card-heading">
              <p className="referentiel-kicker">NOUVEL ÉLÉMENT</p>
              <h3>Créer une ressource</h3>
            </div>

            <form onSubmit={soumettreRessource}>
              <label>
                Nom
                <input
                  name="nom"
                  value={ressourceForm.nom}
                  onChange={modifierRessourceForm}
                  placeholder="Ex. Application transactionnelle"
                  required
                />
              </label>

              <label>
                Type de ressource
                <select
                  name="type_ressource"
                  value={ressourceForm.type_ressource}
                  onChange={modifierRessourceForm}
                >
                  <option value="application">Application</option>
                  <option value="serveur">Serveur</option>
                  <option value="base_de_donnees">
                    Base de données
                  </option>
                  <option value="infrastructure">
                    Infrastructure
                  </option>
                  <option value="personne">Personne</option>
                  <option value="fournisseur">Fournisseur</option>
                  <option value="autre">Autre</option>
                </select>
              </label>

              <label>
                Description
                <textarea
                  name="description"
                  value={ressourceForm.description}
                  onChange={modifierRessourceForm}
                  placeholder="Décrivez la ressource..."
                />
              </label>

              <button className="primary-button" type="submit">
                Créer la ressource
              </button>
            </form>
          </article>

          <article className="referentiel-table-card">
            <div className="card-heading">
              <p className="referentiel-kicker">PATRIMOINE SI</p>
              <h3>Ressources enregistrées</h3>
            </div>

            {ressources.length === 0 ? (
              <div className="empty-referentiel">
                Aucune ressource enregistrée.
              </div>
            ) : (
              <div className="referentiel-table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nom</th>
                      <th>Type</th>
                      <th>Description</th>
                      <th>Statut</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    {ressources.map((ressource) => (
                      <tr key={ressource.id}>
                        <td>#{ressource.id}</td>
                        <td className="strong-cell">{ressource.nom}</td>
                        <td>
                          <span className="type-badge">
                            {ressource.type_ressource}
                          </span>
                        </td>
                        <td>{ressource.description || "—"}</td>
                        <td>
                          <span
                            className={
                              ressource.archive
                                ? "status-badge archived"
                                : "status-badge active-status"
                            }
                          >
                            {ressource.archive ? "Archivée" : "Active"}
                          </span>
                        </td>
                        <td>
                          {!ressource.archive && (
                            <button
                              className="table-action"
                              onClick={() =>
                                traiterArchivageRessource(ressource.id)
                              }
                            >
                              Archiver
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </article>
        </div>
      )}

      {onglet === "dependances" && (
        <div className="referentiel-content">
          <article className="referentiel-form-card">
            <div className="card-heading">
              <p className="referentiel-kicker">RELATION SI</p>
              <h3>Créer une dépendance</h3>
            </div>

            <form onSubmit={soumettreDependance}>
              <label>
                Activité
                <select
                  name="activite_id"
                  value={dependanceForm.activite_id}
                  onChange={modifierDependanceForm}
                  required
                >
                  <option value="">Sélectionner une activité</option>

                  {activites
                    .filter((activite) => !activite.archive)
                    .map((activite) => (
                      <option key={activite.id} value={activite.id}>
                        #{activite.id} — {activite.nom}
                      </option>
                    ))}
                </select>
              </label>

              <label>
                Ressource
                <select
                  name="ressource_id"
                  value={dependanceForm.ressource_id}
                  onChange={modifierDependanceForm}
                  required
                >
                  <option value="">Sélectionner une ressource</option>

                  {ressources
                    .filter((ressource) => !ressource.archive)
                    .map((ressource) => (
                      <option key={ressource.id} value={ressource.id}>
                        #{ressource.id} — {ressource.nom}
                      </option>
                    ))}
                </select>
              </label>

              <label>
                Type de dépendance
                <select
                  name="type_dependance"
                  value={dependanceForm.type_dependance}
                  onChange={modifierDependanceForm}
                >
                  <option value="utilise">Utilise</option>
                  <option value="heberge">Héberge</option>
                  <option value="depend_de">Dépend de</option>
                  <option value="supporte">Supporte</option>
                </select>
              </label>

              <button className="primary-button" type="submit">
                Créer la dépendance
              </button>
            </form>
          </article>

          <article className="referentiel-table-card">
            <div className="card-heading">
              <p className="referentiel-kicker">CARTOGRAPHIE DU SI</p>
              <h3>Dépendances enregistrées</h3>
            </div>

            {dependances.length === 0 ? (
              <div className="empty-referentiel">
                Aucune dépendance enregistrée.
              </div>
            ) : (
              <div className="referentiel-table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Activité</th>
                      <th>Ressource</th>
                      <th>Type</th>
                    </tr>
                  </thead>

                  <tbody>
                    {dependances.map((dependance) => (
                      <tr key={dependance.id}>
                        <td>#{dependance.id}</td>
                        <td>
                          {dependance.activite?.nom ||
                            `Activité #${dependance.activite_id}`}
                        </td>
                        <td>
                          {dependance.ressource?.nom ||
                            `Ressource #${dependance.ressource_id}`}
                        </td>
                        <td>
                          <span className="type-badge">
                            {dependance.type_dependance}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </article>
        </div>
      )}
    </section>
  );
}

export default ReferentielPage;