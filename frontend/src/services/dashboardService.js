const API_URL =
  import.meta.env.VITE_API_URL || "/api/v1";

  
export async function obtenirDashboard() {
  const response = await fetch(`${API_URL}/dashboard`);

  if (!response.ok) {
    throw new Error("Impossible de charger le dashboard.");
  }

  return response.json();
}