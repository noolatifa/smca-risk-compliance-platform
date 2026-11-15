const API_URL = "http://127.0.0.1:8000/api/v1";

export async function telechargerExport(endpoint, nomFichier) {
  const response = await fetch(`${API_URL}${endpoint}`);

  if (!response.ok) {
    const contenu = await response.json().catch(() => null);
    throw new Error(contenu?.detail || "Erreur lors de l'export.");
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const lien = document.createElement("a");

  lien.href = url;
  lien.download = nomFichier;
  document.body.appendChild(lien);
  lien.click();
  lien.remove();

  window.URL.revokeObjectURL(url);
}

export function exporterRisquesCsv() {
  return telechargerExport(
    "/exports/risques.csv",
    "risques.csv",
  );
}

export function exporterRisquesPdf() {
  return telechargerExport(
    "/exports/risques.pdf",
    "risques.pdf",
  );
}

export function exporterTraitementsCsv() {
  return telechargerExport(
    "/exports/traitements.csv",
    "traitements.csv",
  );
}

export function exporterTraitementsPdf() {
  return telechargerExport(
    "/exports/traitements.pdf",
    "traitements.pdf",
  );
}

export function exporterDashboardPdf() {
  return telechargerExport(
    "/exports/dashboard.pdf",
    "dashboard.pdf",
  );
}