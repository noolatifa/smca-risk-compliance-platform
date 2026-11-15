import useCartographie from "../hooks/useCartographie";
import "./CartographiePage.css";

function niveauDepuisScore(score) {
  if (score <= 7) return "faible";
  if (score <= 14) return "modere";
  return "eleve";
}

function classeCellule(probabilite, impact) {
  return `niveau-${niveauDepuisScore(probabilite * impact)}`;
}

export default function CartographiePage() {
  const {
    heatmap,
    statistiques,
    chargement,
    erreur,
    recharger,
  } = useCartographie();

  if (chargement) {
    return <div className="center-page">Chargement de la cartographie...</div>;
  }

  const cellules = heatmap?.cellules || heatmap?.grille || [];

  function obtenirCellule(probabilite, impact) {
    return cellules.find(
      (cellule) =>
        cellule.probabilite === probabilite &&
        cellule.impact === impact,
    );
  }

  return (
    <section className="cartographie-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">ANALYSE DES RISQUES</p>
          <h2>Cartographie des risques</h2>
          <p className="page-subtitle">
            Heatmap 5×5 basée uniquement sur les risques validés.
          </p>
        </div>

        <button className="refresh-button" onClick={recharger}>
          Actualiser
        </button>
      </header>

      {erreur && <div className="cartographie-error">{erreur}</div>}

      <div className="cartographie-grid">
        <section className="panel heatmap-panel">
          <div className="panel-header">
            <p className="panel-kicker">MATRICE DE CRITICITÉ</p>
            <h3>Probabilité × Impact</h3>
          </div>

          <div className="heatmap-wrapper">
            <div className="heatmap-y-label">Probabilité</div>

            <div className="heatmap-content">
              <div className="heatmap">
                {[5, 4, 3, 2, 1].map((probabilite) => (
                  <div className="heatmap-row" key={probabilite}>
                    <span className="axis-number">{probabilite}</span>

                    {[1, 2, 3, 4, 5].map((impact) => {
                      const cellule = obtenirCellule(probabilite, impact);
                      const nombre = cellule?.nombre ?? cellule?.count ?? 0;

                      return (
                        <div
                          className={`heatmap-cell ${classeCellule(
                            probabilite,
                            impact,
                          )}`}
                          key={`${probabilite}-${impact}`}
                          title={`${nombre} risque(s)`}
                        >
                          <strong>{probabilite * impact}</strong>
                          <span>{nombre}</span>
                        </div>
                      );
                    })}
                  </div>
                ))}

                <div className="heatmap-x-axis">
                  <span />
                  {[1, 2, 3, 4, 5].map((impact) => (
                    <span className="axis-number" key={impact}>
                      {impact}
                    </span>
                  ))}
                </div>
              </div>

              <div className="heatmap-x-label">Impact</div>
            </div>
          </div>

          <div className="heatmap-legend">
            <span>
              <i className="legend-low" /> Faible
            </span>
            <span>
              <i className="legend-medium" /> Modéré
            </span>
            <span>
              <i className="legend-high" /> Élevé
            </span>
          </div>
        </section>

        <section className="panel statistics-panel">
          <div className="panel-header">
            <p className="panel-kicker">SYNTHÈSE</p>
            <h3>Statistiques</h3>
          </div>

          <div className="cartographie-statistics">
            <div className="cartographie-stat">
              <span>Total des risques validés</span>
              <strong>
                {statistiques?.total_risques_valides ??
                  statistiques?.total_risques ??
                  0}
              </strong>
            </div>

            <div className="cartographie-stat low">
              <span>Risques faibles</span>
              <strong>
                {statistiques?.risques_faibles ??
                  statistiques?.faibles ??
                  0}
              </strong>
            </div>

            <div className="cartographie-stat medium">
              <span>Risques modérés</span>
              <strong>
                {statistiques?.risques_moderes ??
                  statistiques?.moderes ??
                  0}
              </strong>
            </div>

            <div className="cartographie-stat high">
              <span>Risques élevés</span>
              <strong>
                {statistiques?.risques_eleves ??
                  statistiques?.eleves ??
                  0}
              </strong>
            </div>
          </div>
        </section>
      </div>
    </section>
  );
}