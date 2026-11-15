import useTraitements from "../hooks/useTraitements";
import "./TraitementsPage.css";

function libelleStatut(statut) {
  const statuts = {
    planifie: "Planifié",
    en_cours: "En cours",
    termine: "Terminé",
    annule: "Annulé",
  };

  return statuts[statut] || statut;
}

function estEnRetard(traitement) {
  if (!traitement.echeance || traitement.statut === "termine") {
    return false;
  }

  return new Date(traitement.echeance) < new Date();
}

export default function TraitementsPage() {
  const {
    traitements,
    risques,
    formulaire,
    traitementSelectionne,
    chargement,
    erreur,
    modifierChamp,
    preparerModification,
    reinitialiser,
    enregistrer,
    supprimer,
    recharger,
  } = useTraitements();

  if (chargement) {
    return <div className="center-page">Chargement des traitements...</div>;
  }

  return (
    <section className="traitements-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">PILOTAGE DES MESURES</p>
          <h2>Traitement des risques</h2>
          <p className="page-subtitle">
            Suivez les mesures, les responsables et les échéances.
          </p>
        </div>

        <button className="refresh-button" onClick={recharger}>
          Actualiser
        </button>
      </header>

      {erreur && <div className="traitement-error">{erreur}</div>}

      <div className="traitement-layout">
        <form className="traitement-form" onSubmit={enregistrer}>
          <div className="panel-header">
            <p className="panel-kicker">MESURE</p>
            <h3>
              {traitementSelectionne
                ? "Modifier le traitement"
                : "Ajouter un traitement"}
            </h3>
          </div>

          <label>
            Risque associé
            <select
              name="risque_id"
              value={formulaire.risque_id}
              onChange={modifierChamp}
              required
            >
              <option value="">Sélectionner un risque</option>

              {risques.map((risque) => (
                <option key={risque.id} value={risque.id}>
                  R{risque.id} — {risque.scenario}
                </option>
              ))}
            </select>
          </label>

          <label>
            Mesure
            <input
              name="mesure"
              value={formulaire.mesure}
              onChange={modifierChamp}
              placeholder="Ex : Mettre en place une sauvegarde redondante"
              required
            />
          </label>

          <label>
            Responsable
            <input
              name="responsable"
              value={formulaire.responsable}
              onChange={modifierChamp}
              placeholder="Responsable de la mesure"
              required
            />
          </label>

          <div className="form-row">
            <label>
              Échéance
              <input
                type="date"
                name="echeance"
                value={formulaire.echeance}
                onChange={modifierChamp}
                required
              />
            </label>

            <label>
              Statut
              <select
                name="statut"
                value={formulaire.statut}
                onChange={modifierChamp}
              >
                <option value="planifie">Planifié</option>
                <option value="en_cours">En cours</option>
                <option value="termine">Terminé</option>
                <option value="annule">Annulé</option>
              </select>
            </label>
          </div>

          <label>
            Description
            <textarea
              name="description"
              value={formulaire.description}
              onChange={modifierChamp}
              placeholder="Décrire la mesure à appliquer"
              rows="3"
            />
          </label>

          <label>
            Commentaire
            <textarea
              name="commentaire"
              value={formulaire.commentaire}
              onChange={modifierChamp}
              placeholder="Ajouter une observation"
              rows="3"
            />
          </label>

          {formulaire.statut === "termine" && (
            <label>
              Date de réalisation
              <input
                type="date"
                name="date_realisation"
                value={formulaire.date_realisation}
                onChange={modifierChamp}
                required
              />
            </label>
          )}

          <div className="form-actions">
            <button className="primary-button" type="submit">
              {traitementSelectionne ? "Enregistrer" : "Créer la mesure"}
            </button>

            {traitementSelectionne && (
              <button
                className="secondary-button"
                type="button"
                onClick={reinitialiser}
              >
                Annuler
              </button>
            )}
          </div>
        </form>

        <div className="traitements-list-panel">
          <div className="panel-header">
            <p className="panel-kicker">SUIVI</p>
            <h3>Mesures existantes</h3>
          </div>

          {traitements.length === 0 ? (
            <div className="empty-state">
              <span>✓</span>
              <p>Aucun traitement enregistré.</p>
            </div>
          ) : (
            <div className="traitements-list">
              {traitements.map((traitement) => {
                const retard = estEnRetard(traitement);

                return (
                  <article
                    className={`traitement-card ${
                      retard ? "traitement-card-retard" : ""
                    }`}
                    key={traitement.id}
                  >
                    <div className="traitement-card-top">
                      <span className="traitement-id">
                        T{traitement.id}
                      </span>

                      <span
                        className={`statut-badge statut-${traitement.statut}`}
                      >
                        {libelleStatut(traitement.statut)}
                      </span>
                    </div>

                    <h4>{traitement.mesure}</h4>

                    <p className="traitement-description">
                      {traitement.description || "Aucune description."}
                    </p>

                    <div className="traitement-meta">
                      <span>
                        <strong>Risque :</strong> R{traitement.risque_id}
                      </span>

                      <span>
                        <strong>Responsable :</strong>{" "}
                        {traitement.responsable}
                      </span>

                      <span className={retard ? "date-retard" : ""}>
                        <strong>Échéance :</strong>{" "}
                        {traitement.echeance || "Non définie"}
                        {retard && " — En retard"}
                      </span>
                    </div>

                    <div className="traitement-actions">
                      <button
                        className="small-button"
                        onClick={() => preparerModification(traitement)}
                      >
                        Modifier
                      </button>

                      <button
                        className="small-button danger-button"
                        onClick={() => supprimer(traitement.id)}
                      >
                        Supprimer
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}