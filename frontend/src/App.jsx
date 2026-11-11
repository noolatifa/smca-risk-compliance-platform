import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { obtenirDashboard } from "./services/dashboardService";
import "./App.css";

const COLORS = {
  faible: "#22c55e",
  modere: "#f59e0b",
  eleve: "#ef4444",
};

function MetricCard({ label, value, color }) {
  return (
    <article className="metric-card">
      <div className={`metric-indicator ${color}`}></div>

      <div>
        <p className="metric-label">{label}</p>
        <p className="metric-value">{value}</p>
      </div>
    </article>
  );
}

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function chargerDashboard() {
    try {
      setLoading(true);
      setError("");

      const donnees = await obtenirDashboard();
      setDashboard(donnees);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    chargerDashboard();
  }, []);

  if (loading) {
    return (
      <div className="center-page">
        <p>Chargement du dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="center-page error-page">
        <h2>Erreur de chargement</h2>
        <p>{error}</p>
        <p>
          Vérifie que FastAPI fonctionne sur :
          <br />
          <code>http://127.0.0.1:8000</code>
        </p>
      </div>
    );
  }

  const indicateurs = dashboard.indicateurs;
  const repartition = dashboard.repartition_niveaux || {};
  const risquesParActivite = dashboard.risques_par_activite || [];
  const topRisques = dashboard.top_risques || [];
  const suivi = dashboard.suivi_traitements || {};

  const niveaux = [
    {
      name: "Faible",
      value: repartition.faible || 0,
      key: "faible",
    },
    {
      name: "Modéré",
      value: repartition.modere || 0,
      key: "modere",
    },
    {
      name: "Élevé",
      value: repartition.eleve || 0,
      key: "eleve",
    },
  ];

  const activites = Array.isArray(risquesParActivite)
    ? risquesParActivite.map((item) => ({
        nom: item.activite || item.nom || item.label || "Activité",
        total: item.total || item.nombre || 0,
      }))
    : Object.entries(risquesParActivite).map(([nom, total]) => ({
        nom,
        total,
      }));

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">S</div>

          <div>
            <h1>SMCA</h1>
            <span>Risk Compliance</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <a className="nav-link active" href="#dashboard">
            <span>▦</span>
            Dashboard
          </a>

          <a className="nav-link" href="#referentiel">
            <span>◈</span>
            Référentiel
          </a>

          <a className="nav-link" href="#bia">
            <span>◉</span>
            BIA
          </a>

          <a className="nav-link" href="#risques">
            <span>⚠</span>
            Risques
          </a>

          <a className="nav-link" href="#cartographie">
            <span>▦</span>
            Cartographie
          </a>

          <a className="nav-link" href="#traitements">
            <span>✓</span>
            Traitements
          </a>

          <a className="nav-link" href="#exports">
            <span>⇩</span>
            Exports
          </a>
        </nav>

        <div className="api-status">
          <span></span>
          API connectée
        </div>
      </aside>

      <main className="main-content">
        <header className="page-header">
          <div>
            <p className="eyebrow">VUE GÉNÉRALE</p>
            <h2>Tableau de bord</h2>
            <p className="page-subtitle">
              Synthèse des risques et des plans de traitement.
            </p>
          </div>

          <button className="refresh-button" onClick={chargerDashboard}>
            Actualiser
          </button>
        </header>

        <section className="metrics-grid">
          <MetricCard
            label="Risques totaux"
            value={indicateurs.total_risques}
            color="blue"
          />

          <MetricCard
            label="Risques élevés"
            value={indicateurs.risques_eleves}
            color="red"
          />

          <MetricCard
            label="Risques modérés"
            value={indicateurs.risques_moderees}
            color="orange"
          />

          <MetricCard
            label="Risques faibles"
            value={indicateurs.risques_faibles}
            color="green"
          />

          <MetricCard
            label="Mesures en retard"
            value={indicateurs.mesures_en_retard}
            color="purple"
          />
        </section>

        <section className="dashboard-grid">
          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="panel-kicker">ANALYSE DES RISQUES</p>
                <h3>Répartition par niveau</h3>
              </div>
            </div>

            {indicateurs.total_risques === 0 ? (
              <div className="empty-state">
                <span>○</span>
                <p>Aucun risque enregistré.</p>
              </div>
            ) : (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={260}>
                  <PieChart>
                    <Pie
                      data={niveaux}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      innerRadius={65}
                      outerRadius={95}
                      paddingAngle={4}
                    >
                      {niveaux.map((niveau) => (
                        <Cell
                          key={niveau.key}
                          fill={COLORS[niveau.key]}
                        />
                      ))}
                    </Pie>

                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </article>

          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="panel-kicker">CARTOGRAPHIE</p>
                <h3>Risques par activité</h3>
              </div>
            </div>

            {activites.length === 0 ? (
              <div className="empty-state">
                <span>○</span>
                <p>Aucune activité concernée.</p>
              </div>
            ) : (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart
                    data={activites}
                    layout="vertical"
                    margin={{
                      top: 10,
                      right: 20,
                      left: 20,
                      bottom: 10,
                    }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      horizontal={false}
                    />

                    <XAxis type="number" allowDecimals={false} />
                    <YAxis dataKey="nom" type="category" width={120} />
                    <Tooltip />

                    <Bar
                      dataKey="total"
                      name="Risques"
                      fill="#2563eb"
                      radius={[0, 6, 6, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </article>
        </section>

        <section className="dashboard-grid">
          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="panel-kicker">PRIORISATION</p>
                <h3>Top 3 des risques</h3>
              </div>
            </div>

            {topRisques.length === 0 ? (
              <div className="empty-state">
                <span>○</span>
                <p>Aucun risque prioritaire.</p>
              </div>
            ) : (
              <div className="risk-list">
                {topRisques.slice(0, 3).map((risque) => (
                  <div className="risk-row" key={risque.id}>
                    <div className="risk-id">R{risque.id}</div>

                    <div className="risk-information">
                      <strong>{risque.scenario}</strong>
                      <span>{risque.proprietaire}</span>
                    </div>

                    <div className={`risk-score ${risque.niveau}`}>
                      {risque.score_criticite}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </article>

          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="panel-kicker">PLAN DE TRAITEMENT</p>
                <h3>Suivi des mesures</h3>
              </div>
            </div>

            <div className="treatment-list">
              <div className="treatment-row">
                <span className="treatment-dot gray"></span>
                <span>Planifiées</span>
                <strong>{suivi.planifies || 0}</strong>
              </div>

              <div className="treatment-row">
                <span className="treatment-dot blue"></span>
                <span>En cours</span>
                <strong>{suivi.en_cours || 0}</strong>
              </div>

              <div className="treatment-row">
                <span className="treatment-dot green"></span>
                <span>Terminées</span>
                <strong>{suivi.termines || 0}</strong>
              </div>

              <div className="treatment-row">
                <span className="treatment-dot red"></span>
                <span>En retard</span>
                <strong className="danger">{suivi.en_retard || 0}</strong>
              </div>
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}

export default App;