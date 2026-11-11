const API_URL = "http://127.0.0.1:8000/api/v1";

export async function obtenirDashboard() {
  const response = await fetch(`${API_URL}/dashboard`);

  if (!response.ok) {
    throw new Error("Impossible de charger le dashboard.");
  }

  return response.json();
}