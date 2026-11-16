import { useEffect, useState } from "react";

import Sidebar from "../components/common/Sidebar";
import DashboardPage from "../features/dashboard/pages/DashboardPage";
import ReferentielPage from "../features/processus/pages/referentielPage";
import BiaPage from "../features/bia/pages/BiaPage";
import RisquesPage from "../features/risques/pages/RisquesPage";
import TraitementsPage from "../features/traitement/pages/TraitementsPage";
import CartographiePage from "../features/cartographie/pages/CartographiePage";
import ExportsPage from "../features/exports/pages/ExportsPage";

import { obtenirDashboard } from "../services/dashboardService";

export default function AppLayout() {
  const [page, setPage] = useState("dashboard");
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

  function afficherPage() {
    if (page === "referentiel") {
      return <ReferentielPage />;
    }

    if (page === "bia") {
      return <BiaPage />;
    }

    if (page === "risques") {
      return <RisquesPage />;
    }

    if (page === "traitements") {
      return <TraitementsPage />;
    }

    if (page === "cartographie") {
      return <CartographiePage />;
    }

    if (page === "exports") {
      return <ExportsPage />;
    }

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

    return (
      <DashboardPage
        dashboard={dashboard}
        onRefresh={chargerDashboard}
      />
    );
  }

  return (
    <div className="app-layout">
      <Sidebar
        page={page}
        setPage={setPage}
      />

      <main className="main-content">
        {afficherPage()}
      </main>
    </div>
  );
}