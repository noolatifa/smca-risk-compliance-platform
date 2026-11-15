import { useState } from "react";
import {
  exporterDashboardPdf,
  exporterRisquesCsv,
  exporterRisquesPdf,
  exporterTraitementsCsv,
  exporterTraitementsPdf,
} from "../services/exportsService";
import "./ExportsPage.css";

export default function ExportsPage() {
  const [chargement, setChargement] = useState("");
  const [erreur, setErreur] = useState("");
  const [succes, setSucces] = useState("");

  async function lancerExport(nom, fonctionExport) {
    try {
      setChargement(nom);
      setErreur("");
      setSucces("");

      await fonctionExport();

      setSucces("Le fichier a été téléchargé.");
    } catch (error) {
      setErreur(error.message);
    } finally {
      setChargement("");
    }
  }

  function boutonExport(id, titre, description, fonctionExport) {
    return (
      <article className="export-card">
        <div className="export-icon">{id}</div>

        <div className="export-information">
          <h3>{titre}</h3>
          <p>{description}</p>
        </div>

        <button
          className="export-button"
          disabled={chargement !== ""}
          onClick={() => lancerExport(id, fonctionExport)}
        >
          {chargement === id ? "Téléchargement..." : "Télécharger"}
        </button>
      </article>
    );
  }

  return (
    <section className="exports-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">DOCUMENTATION ET REPORTING</p>
          <h2>Exports</h2>
          <p className="page-subtitle">
            Téléchargez les données et les rapports de conformité.
          </p>
        </div>
      </header>

      {erreur && <div className="exports-error">{erreur}</div>}
      {succes && <div className="exports-success">{succes}</div>}

      <div className="exports-list">
        {boutonExport(
          "RC",
          "Risques — CSV",
          "Exporter les risques validés dans un fichier CSV.",
          exporterRisquesCsv,
        )}

        {boutonExport(
          "RP",
          "Risques — PDF",
          "Générer un rapport PDF des risques validés.",
          exporterRisquesPdf,
        )}

        {boutonExport(
          "TC",
          "Traitements — CSV",
          "Exporter les mesures de traitement dans un fichier CSV.",
          exporterTraitementsCsv,
        )}

        {boutonExport(
          "TP",
          "Traitements — PDF",
          "Générer un rapport PDF des traitements.",
          exporterTraitementsPdf,
        )}

        {boutonExport(
          "DB",
          "Dashboard — PDF",
          "Générer une synthèse PDF du tableau de bord.",
          exporterDashboardPdf,
        )}
      </div>
    </section>
  );
}