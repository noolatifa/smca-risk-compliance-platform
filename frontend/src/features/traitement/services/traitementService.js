const API_URL = "http://127.0.0.1:8000/api/v1";

async function traiterReponse(response) {
  const contenu = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(contenu?.detail || "Erreur avec l'API.");
  }

  return contenu;
}

export async function listerTraitements() {
  const response = await fetch(`${API_URL}/traitements`);
  return traiterReponse(response);
}

export async function creerTraitement(donnees) {
  const response = await fetch(`${API_URL}/traitements`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}

export async function modifierTraitement(id, donnees) {
  const response = await fetch(`${API_URL}/traitements/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}

export async function supprimerTraitement(id) {
  const response = await fetch(`${API_URL}/traitements/${id}`, {
    method: "DELETE",
  });

  return traiterReponse(response);
}

export async function listerTraitementsEnRetard() {
  const response = await fetch(`${API_URL}/traitements/en-retard`);
  return traiterReponse(response);
}

export async function obtenirDashboardTraitements() {
  const response = await fetch(`${API_URL}/traitements/dashboard`);
  return traiterReponse(response);
}

export async function listerRisques() {
  const response = await fetch(`${API_URL}/risques`);
  return traiterReponse(response);
}