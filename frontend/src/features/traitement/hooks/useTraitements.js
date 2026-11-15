import { useCallback, useEffect, useState } from "react";
import {
  creerTraitement,
  listerRisques,
  listerTraitements,
  modifierTraitement,
  supprimerTraitement,
} from "../services/traitementService";

const formulaireInitial = {
  risque_id: "",
  mesure: "",
  responsable: "",
  echeance: "",
  statut: "planifie",
  description: "",
  commentaire: "",
  date_realisation: "",
};

export default function useTraitements() {
  const [traitements, setTraitements] = useState([]);
  const [risques, setRisques] = useState([]);
  const [formulaire, setFormulaire] = useState(formulaireInitial);
  const [traitementSelectionne, setTraitementSelectionne] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState("");

  const chargerDonnees = useCallback(async () => {
    try {
      setChargement(true);
      setErreur("");

      const [traitementsData, risquesData] = await Promise.all([
        listerTraitements(),
        listerRisques(),
      ]);

      setTraitements(traitementsData);
      setRisques(risquesData);
    } catch (error) {
      setErreur(error.message);
    } finally {
      setChargement(false);
    }
  }, []);

  useEffect(() => {
    chargerDonnees();
  }, [chargerDonnees]);

  function modifierChamp(event) {
    const { name, value } = event.target;

    setFormulaire((ancien) => ({
      ...ancien,
      [name]: value,
    }));
  }

  function preparerModification(traitement) {
    setTraitementSelectionne(traitement);

    setFormulaire({
      risque_id: traitement.risque_id ?? "",
      mesure: traitement.mesure ?? "",
      responsable: traitement.responsable ?? "",
      echeance: traitement.echeance ?? "",
      statut: traitement.statut ?? "planifie",
      description: traitement.description ?? "",
      commentaire: traitement.commentaire ?? "",
      date_realisation: traitement.date_realisation ?? "",
    });
  }

  function reinitialiser() {
    setTraitementSelectionne(null);
    setFormulaire(formulaireInitial);
  }

  async function enregistrer(event) {
    event.preventDefault();

    try {
      setErreur("");

      const donnees = {
        risque_id: Number(formulaire.risque_id),
        mesure: formulaire.mesure,
        responsable: formulaire.responsable,
        echeance: formulaire.echeance,
        statut: formulaire.statut,
        description: formulaire.description || null,
        commentaire: formulaire.commentaire || null,
        date_realisation: formulaire.date_realisation || null,
      };

      if (traitementSelectionne) {
        await modifierTraitement(traitementSelectionne.id, donnees);
      } else {
        await creerTraitement(donnees);
      }

      reinitialiser();
      await chargerDonnees();
    } catch (error) {
      setErreur(error.message);
    }
  }

  async function supprimer(id) {
    if (!window.confirm("Supprimer ce traitement ?")) {
      return;
    }

    try {
      setErreur("");
      await supprimerTraitement(id);
      await chargerDonnees();
    } catch (error) {
      setErreur(error.message);
    }
  }

  return {
    traitements,
    risques,
    formulaire,
    traitementSelectionne,
    chargement,
    erreur,
    modifierChamp,
    preparerModification,
    reinitialiser,
    enregistrer,
    supprimer,
    recharger: chargerDonnees,
  };
}