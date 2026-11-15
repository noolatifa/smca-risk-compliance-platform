const API_URL = "http://127.0.0.1:8000/api/v1";

async function traiterReponse(response) {
  const contenu = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(contenu?.detail || "Erreur avec l'API.");
  }

  return contenu;
}

export async function obtenirHeatmap() {
  const response = await fetch(`${API_URL}/cartographie/heatmap`);
  return traiterReponse(response);
}

export async function obtenirStatistiques() {
  const response = await fetch(`${API_URL}/cartographie/statistiques`);
  return traiterReponse(response);
}