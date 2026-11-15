import { useCallback, useEffect, useState } from "react";
import {
  obtenirHeatmap,
  obtenirStatistiques,
} from "../services/cartographieService";

export default function useCartographie() {
  const [heatmap, setHeatmap] = useState(null);
  const [statistiques, setStatistiques] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState("");

  const chargerDonnees = useCallback(async () => {
    try {
      setChargement(true);
      setErreur("");

      const [heatmapData, statistiquesData] = await Promise.all([
        obtenirHeatmap(),
        obtenirStatistiques(),
      ]);

      setHeatmap(heatmapData);
      setStatistiques(statistiquesData);
    } catch (error) {
      setErreur(error.message);
    } finally {
      setChargement(false);
    }
  }, []);

  useEffect(() => {
    chargerDonnees();
  }, [chargerDonnees]);

  return {
    heatmap,
    statistiques,
    chargement,
    erreur,
    recharger: chargerDonnees,
  };
}