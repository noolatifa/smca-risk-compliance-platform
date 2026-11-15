const API_URL = "http://127.0.0.1:8000/api/v1";

async function traiterReponse(response) {
  const contenu = await response.json().catch(() => null);

  if (!response.ok) {
    const message =
      contenu?.detail || "Une erreur est survenue avec l'API.";

    throw new Error(message);
  }

  return contenu;
}

export async function listerActivites(inclureArchives = false) {
  const response = await fetch(
    `${API_URL}/activites?inclure_archives=${inclureArchives}`,
  );

  return traiterReponse(response);
}

export async function creerActivite(donnees) {
  const response = await fetch(`${API_URL}/activites`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}

export async function obtenirActivite(id) {
  const response = await fetch(`${API_URL}/activites/${id}`);

  return traiterReponse(response);
}

export async function archiverActivite(id) {
  const response = await fetch(`${API_URL}/activites/${id}/archiver`, {
    method: "POST",
  });

  return traiterReponse(response);
}

export async function listerRessources(inclureArchives = false) {
  const response = await fetch(
    `${API_URL}/ressources?inclure_archives=${inclureArchives}`,
  );

  return traiterReponse(response);
}

export async function creerRessource(donnees) {
  const response = await fetch(`${API_URL}/ressources`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}

export async function obtenirRessource(id) {
  const response = await fetch(`${API_URL}/ressources/${id}`);

  return traiterReponse(response);
}

export async function archiverRessource(id) {
  const response = await fetch(`${API_URL}/ressources/${id}/archiver`, {
    method: "POST",
  });

  return traiterReponse(response);
}

export async function listerDependances() {
  const response = await fetch(`${API_URL}/dependances`);

  return traiterReponse(response);
}

export async function creerDependance(donnees) {
  const response = await fetch(`${API_URL}/dependances`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(donnees),
  });

  return traiterReponse(response);
}