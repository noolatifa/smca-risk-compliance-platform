import { useBia } from "../hooks/useBia";
import "./BiaPage.css";

const STATUTS = {
  brouillon: "Brouillon",
  soumis: "Soumis",
  valide: "Validé",
  a_corriger: "À corriger",
};

function BiaPage() {
  const {
    bias,
    activites,
    formulaire,
    biaSelectionnee,
    chargement,
    erreur,
    message,
    modifierChamp,
    modifierImpact,
    ajouterImpact,
    supprimerImpact,
    selectionnerBia,
    reinitialiserFormulaire,
    enregistrerBia,
    soumettre,
    valider,
    corriger,
  } = useBia();

  if (chargement) {
    return (
      <div className="bia-state">
        Chargement des analyses BIA...
      </div>
    );
  }

  return (
    <section className="bia-page">
      <header className="bia-header">
        <div>
          <p className="bia-kicker">CONTINUITÉ D’ACTIVITÉ</p>
          <h2>Business Impact Analysis</h2>
          <p>
            Évaluez les impacts d’une interruption et définissez les
            objectifs de continuité.
          </p>
        </div>

        <button
          className="bia-secondary-button"
          onClick={reinitialiserFormulaire}
        >
          Nouvelle BIA
        </button>
      </header>

      {erreur && <div className="bia-alert error">{erreur}</div>}
      {message && <div className="bia-alert success">{message}</div>}

      <div className="bia-layout">
        <aside className="bia-list-card">
          <div className="bia-card-title">
            <p className="bia-kicker">ANALYSES EXISTANTES</p>
            <h3>BIA enregistrées</h3>
          </div>

          {bias.length === 0 ? (
            <div className="bia-empty">
              Aucune BIA enregistrée.
            </div>
          ) : (
            <div className="bia-list">
              {bias.map((bia) => {
                const activite = activites.find(
                  (item) => item.id === bia.activite_id,
                );

                return (
                  <button
                    type="button"
                    key={bia.id}
                    className={`bia-list-item ${
                      biaSelectionnee?.id === bia.id ? "selected" : ""
                    }`}
                    onClick={() => selectionnerBia(bia)}
                  >
                    <span className="bia-list-id">BIA-{bia.id}</span>

                    <span className="bia-list-name">
                      {activite?.nom ||
                        `Activité #${bia.activite_id}`}
                    </span>

                    <span
                      className={`bia-status ${bia.statut}`}
                    >
                      {STATUTS[bia.statut] || bia.statut}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </aside>

        <form className="bia-form-card" onSubmit={enregistrerBia}>
          <div className="bia-card-title">
            <p className="bia-kicker">
              {biaSelectionnee ? "MODIFICATION" : "NOUVELLE ANALYSE"}
            </p>

            <h3>
              {biaSelectionnee
                ? `BIA-${biaSelectionnee.id}`
                : "Créer une BIA"}
            </h3>
          </div>

          <fieldset>
            <legend>Contexte de l’activité</legend>

            <div className="bia-form-grid">
              <label>
                Activité
                <select
                  name="activite_id"
                  value={formulaire.activite_id}
                  onChange={modifierChamp}
                  disabled={Boolean(biaSelectionnee)}
                  required
                >
                  <option value="">Sélectionner une activité</option>

                  {activites
                    .filter((activite) => !activite.archive)
                    .map((activite) => (
                      <option
                        key={activite.id}
                        value={activite.id}
                      >
                        #{activite.id} — {activite.nom}
                      </option>
                    ))}
                </select>
              </label>

              <label>
                Responsable
                <input
                  name="responsable"
                  value={formulaire.responsable}
                  onChange={modifierChamp}
                  placeholder="Responsable métier"
                />
              </label>

              <label>
                Heures de fonctionnement
                <input
                  name="heures_fonctionnement"
                  value={formulaire.heures_fonctionnement}
                  onChange={modifierChamp}
                  placeholder="Ex. 08:00 - 18:00"
                />
              </label>

              <label>
                Période de pointe
                <input
                  name="periode_pointe"
                  value={formulaire.periode_pointe}
                  onChange={modifierChamp}
                  placeholder="Ex. Fin de mois"
                />
              </label>

              <label className="full-width">
                Sites concernés
                <textarea
                  name="sites_concernes"
                  value={formulaire.sites_concernes}
                  onChange={modifierChamp}
                  placeholder="Sites, agences ou environnements concernés"
                />
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>Objectifs de continuité</legend>

            <div className="bia-form-grid">
              <label>
                MTPD — heures
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  name="mtpd_heures"
                  value={formulaire.mtpd_heures}
                  onChange={modifierChamp}
                  placeholder="Ex. 24"
                />
              </label>

              <label>
                RTO — heures
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  name="rto_heures"
                  value={formulaire.rto_heures}
                  onChange={modifierChamp}
                  placeholder="Ex. 4"
                />
              </label>

              <label>
                RPO — heures
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  name="rpo_heures"
                  value={formulaire.rpo_heures}
                  onChange={modifierChamp}
                  placeholder="Ex. 1"
                />
              </label>

              <label>
                Capacité minimale — %
                <input
                  type="number"
                  min="1"
                  max="100"
                  name="capacite_minimale_pct"
                  value={formulaire.capacite_minimale_pct}
                  onChange={modifierChamp}
                  placeholder="Ex. 60"
                />
              </label>

              <label className="full-width">
                Justification MTPD
                <textarea
                  name="justification_mtpd"
                  value={formulaire.justification_mtpd}
                  onChange={modifierChamp}
                />
              </label>

              <label className="full-width">
                Justification RPO
                <textarea
                  name="justification_rpo"
                  value={formulaire.justification_rpo}
                  onChange={modifierChamp}
                />
              </label>
            </div>
          </fieldset>

          <fieldset>
            <div className="fieldset-heading">
              <legend>Impacts selon l’horizon</legend>

              <button
                type="button"
                className="small-button"
                onClick={ajouterImpact}
              >
                Ajouter un horizon
              </button>
            </div>

            <div className="impact-list">
              {formulaire.impacts.map((impact, index) => (
                <div className="impact-card" key={index}>
                  <div className="impact-header">
                    <strong>Horizon {index + 1}</strong>

                    {formulaire.impacts.length > 1 && (
                      <button
                        type="button"
                        className="remove-button"
                        onClick={() => supprimerImpact(index)}
                      >
                        Supprimer
                      </button>
                    )}
                  </div>

                  <div className="bia-form-grid">
                    <label>
                      Horizon
                      <select
                        name="horizon_heures"
                        value={impact.horizon_heures}
                        onChange={(event) =>
                          modifierImpact(index, event)
                        }
                      >
                        <option value="1">1 heure</option>
                        <option value="4">4 heures</option>
                        <option value="8">8 heures</option>
                        <option value="24">24 heures</option>
                        <option value="72">72 heures</option>
                      </select>
                    </label>

                    <label>
                      Clients
                      <textarea
                        name="clients"
                        value={impact.clients}
                        onChange={(event) =>
                          modifierImpact(index, event)
                        }
                      />
                    </label>

                    <label>
                      Opérations
                      <textarea
                        name="operations"
                        value={impact.operations}
                        onChange={(event) =>
                          modifierImpact(index, event)
                        }
                      />
                    </label>

                    <label>
                      Finances
                      <textarea
                        name="finances"
                        value={impact.finances}
                        onChange={(event) =>
                          modifierImpact(index, event)
                        }
                      />
                    </label>

                    <label>
                      Engagements
                      <textarea
                        name="engagements"
                        value={impact.engagements}
                        onChange={(event) =>
                          modifierImpact(index, event)
                        }
                      />
                    </label>

                    <label>
                      Réputation
                      <textarea
                        name="reputation"
                        value={impact.reputation}
                        onChange={(event) =>
                          modifierImpact(index, event)
                        }
                      />
                    </label>
                  </div>
                </div>
              ))}
            </div>
          </fieldset>

          <div className="bia-actions">
            <button className="bia-primary-button" type="submit">
              {biaSelectionnee ? "Enregistrer les modifications" : "Créer la BIA"}
            </button>

            {biaSelectionnee && (
              <>
                {biaSelectionnee.statut === "brouillon" ||
                biaSelectionnee.statut === "a_corriger" ? (
                  <button
                    type="button"
                    className="bia-secondary-button"
                    onClick={() => soumettre(biaSelectionnee.id)}
                  >
                    Soumettre
                  </button>
                ) : null}

                {biaSelectionnee.statut === "soumis" ? (
                  <>
                    <button
                      type="button"
                      className="bia-primary-button"
                      onClick={() => valider(biaSelectionnee.id)}
                    >
                      Valider
                    </button>

                    <button
                      type="button"
                      className="bia-warning-button"
                      onClick={() => corriger(biaSelectionnee.id)}
                    >
                      Demander une correction
                    </button>
                  </>
                ) : null}
              </>
            )}
          </div>
        </form>
      </div>
    </section>
  );
}

export default BiaPage;