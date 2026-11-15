const API_URL = "http://127.0.0.1:8000/api/v1";

async function traiterReponse(response) {
  const contenu = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      contenu?.detail || "Une erreur est survenue avec l'API.",
    );
  }

  return contenu;
}

export async function listerRisques() {
  const response = await fetch(`${API_URL}/risques`);
  return traiterReponse(response);
}

export async function creerRisque(donnees) {
  const response = await fetch(`${API_URL}/risques`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}

export async function modifierRisque(id, donnees) {
  const response = await fetch(`${API_URL}/risques/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}

export async function soumettreRisque(id) {
  const response = await fetch(`${API_URL}/risques/${id}/soumettre`, {
    method: "POST",
  });

  return traiterReponse(response);
}

export async function validerRisque(id) {
  const response = await fetch(`${API_URL}/risques/${id}/valider`, {
    method: "POST",
  });

  return traiterReponse(response);
}

export async function corrigerRisque(id) {
  const response = await fetch(`${API_URL}/risques/${id}/a-corriger`, {
    method: "POST",
  });

  return traiterReponse(response);
}

export async function listerActivites() {
  const response = await fetch(`${API_URL}/activites`);
  return traiterReponse(response);
}

export async function listerRessources() {
  const response = await fetch(`${API_URL}/ressources`);
  return traiterReponse(response);
}