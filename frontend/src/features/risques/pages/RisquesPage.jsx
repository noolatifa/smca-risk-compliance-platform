import { useRisques } from "../hooks/useRisques";
import "./RisquesPage.css";

const STATUTS = {
  brouillon: "Brouillon",
  soumis: "Soumis",
  valide: "Validé",
  a_corriger: "À corriger",
};

function RisquesPage() {
  const {
    risques,
    activites,
    ressources,
    formulaire,
    risqueSelectionne,
    chargement,
    erreur,
    message,
    modifierChamp,
    modifierSelection,
    selectionnerRisque,
    nouveauRisque,
    enregistrer,
    soumettre,
    valider,
    corriger,
  } = useRisques();

  if (chargement) {
    return (
      <div className="risques-state">
        Chargement des risques...
      </div>
    );
  }

  const score =
    Number(formulaire.probabilite) * Number(formulaire.impact);

  const niveau =
    score <= 7 ? "faible" : score <= 14 ? "modere" : "eleve";

  const risqueValide = risqueSelectionne?.statut === "valide";

  return (
    <section className="risques-page">
      <header className="risques-header">
        <div>
          <p className="risques-kicker">ANALYSE ET ÉVALUATION</p>
          <h2>Gestion des risques</h2>
          <p>
            Identifiez, évaluez et suivez les risques de votre système.
          </p>
        </div>

        <button className="risque-secondary-button" onClick={nouveauRisque}>
          Nouveau risque
        </button>
      </header>

      {erreur && <div className="risque-alert error">{erreur}</div>}
      {message && (
        <div className="risque-alert success">{message}</div>
      )}

      <div className="risques-layout">
        <aside className="risques-list-card">
          <div className="risque-card-title">
            <p className="risques-kicker">REGISTRE DES RISQUES</p>
            <h3>Risques enregistrés</h3>
          </div>

          {risques.length === 0 ? (
            <div className="risque-empty">
              Aucun risque enregistré.
            </div>
          ) : (
            <div className="risques-list">
              {risques.map((risque) => (
                <button
                  type="button"
                  key={risque.id}
                  className={`risque-list-item ${
                    risqueSelectionne?.id === risque.id
                      ? "selected"
                      : ""
                  }`}
                  onClick={() => selectionnerRisque(risque)}
                >
                  <span className="risque-list-top">
                    R{risque.id}
                    <strong>{risque.score_criticite}</strong>
                  </span>

                  <span className="risque-list-scenario">
                    {risque.scenario}
                  </span>

                  <span className={`risk-badge ${risque.niveau}`}>
                    {risque.niveau}
                  </span>

                  <span className="risk-status">
                    {STATUTS[risque.statut] || risque.statut}
                  </span>
                </button>
              ))}
            </div>
          )}
        </aside>

        <form className="risque-form-card" onSubmit={enregistrer}>
          <div className="risque-card-title">
            <p className="risques-kicker">
              {risqueSelectionne ? "MODIFICATION" : "NOUVELLE ÉVALUATION"}
            </p>
            <h3>
              {risqueSelectionne
                ? `Risque R${risqueSelectionne.id}`
                : "Créer un risque"}
            </h3>
          </div>

          <div className="risque-form-grid">
            <label className="full-width">
              Scénario
              <textarea
                name="scenario"
                value={formulaire.scenario}
                onChange={modifierChamp}
                placeholder="Décrivez le scénario de risque..."
                required
                disabled={risqueValide}
              />
            </label>

            <label>
              Cause
              <textarea
                name="cause"
                value={formulaire.cause}
                onChange={modifierChamp}
                required
                disabled={risqueValide}
              />
            </label>

            <label>
              Menace
              <textarea
                name="menace"
                value={formulaire.menace}
                onChange={modifierChamp}
                required
                disabled={risqueValide}
              />
            </label>

            <label>
              Vulnérabilité
              <textarea
                name="vulnerabilite"
                value={formulaire.vulnerabilite}
                onChange={modifierChamp}
                required
                disabled={risqueValide}
              />
            </label>

            <label>
              Conséquences
              <textarea
                name="consequences"
                value={formulaire.consequences}
                onChange={modifierChamp}
                required
                disabled={risqueValide}
              />
            </label>

            <label>
              Propriétaire
              <input
                name="proprietaire"
                value={formulaire.proprietaire}
                onChange={modifierChamp}
                required
                disabled={risqueValide}
              />
            </label>

            <label>
              Probabilité
              <select
                name="probabilite"
                value={formulaire.probabilite}
                onChange={modifierChamp}
                disabled={risqueValide}
              >
                {[1, 2, 3, 4, 5].map((valeur) => (
                  <option key={valeur} value={valeur}>
                    {valeur} / 5
                  </option>
                ))}
              </select>
            </label>

            <label>
              Impact
              <select
                name="impact"
                value={formulaire.impact}
                onChange={modifierChamp}
                disabled={risqueValide}
              >
                {[1, 2, 3, 4, 5].map((valeur) => (
                  <option key={valeur} value={valeur}>
                    {valeur} / 5
                  </option>
                ))}
              </select>
            </label>

            <div className={`score-preview ${niveau}`}>
              <span>Score de criticité</span>
              <strong>{score}</strong>
              <small>{niveau}</small>
            </div>
          </div>

          <fieldset>
            <legend>Activités concernées</legend>

            <div className="checkbox-grid">
              {activites
                .filter((activite) => !activite.archive)
                .map((activite) => (
                  <label className="checkbox-item" key={activite.id}>
                    <input
                      type="checkbox"
                      checked={formulaire.activite_ids.includes(
                        activite.id,
                      )}
                      onChange={() =>
                        modifierSelection(
                          "activite_ids",
                          activite.id,
                        )
                      }
                      disabled={risqueValide}
                    />
                    {activite.nom}
                  </label>
                ))}
            </div>
          </fieldset>

          <fieldset>
            <legend>Ressources concernées</legend>

            <div className="checkbox-grid">
              {ressources
                .filter((ressource) => !ressource.archive)
                .map((ressource) => (
                  <label className="checkbox-item" key={ressource.id}>
                    <input
                      type="checkbox"
                      checked={formulaire.ressource_ids.includes(
                        ressource.id,
                      )}
                      onChange={() =>
                        modifierSelection(
                          "ressource_ids",
                          ressource.id,
                        )
                      }
                      disabled={risqueValide}
                    />
                    {ressource.nom}
                  </label>
                ))}
            </div>
          </fieldset>

          <div className="risque-actions">
            {!risqueValide && (
              <button className="risque-primary-button" type="submit">
                {risqueSelectionne
                  ? "Enregistrer les modifications"
                  : "Créer le risque"}
              </button>
            )}

            {risqueSelectionne?.statut === "brouillon" ||
            risqueSelectionne?.statut === "a_corriger" ? (
              <button
                type="button"
                className="risque-secondary-button"
                onClick={() => soumettre(risqueSelectionne.id)}
              >
                Soumettre
              </button>
            ) : null}

            {risqueSelectionne?.statut === "soumis" ? (
              <>
                <button
                  type="button"
                  className="risque-primary-button"
                  onClick={() => valider(risqueSelectionne.id)}
                >
                  Valider
                </button>

                <button
                  type="button"
                  className="risque-warning-button"
                  onClick={() => corriger(risqueSelectionne.id)}
                >
                  Demander une correction
                </button>
              </>
            ) : null}
          </div>
        </form>
      </div>
    </section>
  );
}

export default RisquesPage;