import { useCallback, useEffect, useState } from "react";

import {
  corrigerRisque,
  creerRisque,
  listerActivites,
  listerRessources,
  listerRisques,
  modifierRisque,
  soumettreRisque,
  validerRisque,
} from "../services/risquesService";

function formulaireVide() {
  return {
    scenario: "",
    cause: "",
    menace: "",
    vulnerabilite: "",
    consequences: "",
    proprietaire: "",
    activite_ids: [],
    ressource_ids: [],
    probabilite: 1,
    impact: 1,
  };
}

function convertirRisqueEnFormulaire(risque) {
  return {
    scenario: risque.scenario || "",
    cause: risque.cause || "",
    menace: risque.menace || "",
    vulnerabilite: risque.vulnerabilite || "",
    consequences: risque.consequences || "",
    proprietaire: risque.proprietaire || "",
    activite_ids: risque.activite_ids || [],
    ressource_ids: risque.ressource_ids || [],
    probabilite: risque.probabilite,
    impact: risque.impact,
  };
}

export function useRisques() {
  const [risques, setRisques] = useState([]);
  const [activites, setActivites] = useState([]);
  const [ressources, setRessources] = useState([]);
  const [formulaire, setFormulaire] = useState(formulaireVide());
  const [risqueSelectionne, setRisqueSelectionne] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState("");
  const [message, setMessage] = useState("");

  const chargerDonnees = useCallback(async () => {
    try {
      setChargement(true);
      setErreur("");

      const [risquesData, activitesData, ressourcesData] =
        await Promise.all([
          listerRisques(),
          listerActivites(),
          listerRessources(),
        ]);

      setRisques(risquesData);
      setActivites(activitesData);
      setRessources(ressourcesData);
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

  function modifierSelection(name, value) {
    setFormulaire((ancien) => ({
      ...ancien,
      [name]: ancien[name].includes(value)
        ? ancien[name].filter((id) => id !== value)
        : [...ancien[name], value],
    }));
  }

  function selectionnerRisque(risque) {
    setRisqueSelectionne(risque);
    setFormulaire(convertirRisqueEnFormulaire(risque));
    setErreur("");
    setMessage("");
  }

  function nouveauRisque() {
    setRisqueSelectionne(null);
    setFormulaire(formulaireVide());
    setErreur("");
    setMessage("");
  }

  async function enregistrer(event) {
    event.preventDefault();

    try {
      setErreur("");
      setMessage("");

      const donnees = {
        ...formulaire,
        probabilite: Number(formulaire.probabilite),
        impact: Number(formulaire.impact),
        activite_ids: formulaire.activite_ids.map(Number),
        ressource_ids: formulaire.ressource_ids.map(Number),
      };

      if (risqueSelectionne) {
        await modifierRisque(risqueSelectionne.id, donnees);
        setMessage("Risque modifié avec succès.");
      } else {
        await creerRisque(donnees);
        setMessage("Risque créé avec succès.");
      }

      await chargerDonnees();
      nouveauRisque();
    } catch (error) {
      setErreur(error.message);
    }
  }

  async function action(actionFonction, id, texte) {
    try {
      setErreur("");
      setMessage("");

      await actionFonction(id);
      setMessage(texte);
      await chargerDonnees();
    } catch (error) {
      setErreur(error.message);
    }
  }

  return {
    risques,
    activites,
    ressources,
    formulaire,
    risqueSelectionne,
    chargement,
    erreur,
    message,
    modifierChamp,
    modifierSelection,
    selectionnerRisque,
    nouveauRisque,
    enregistrer,
    soumettre: (id) =>
      action(
        soumettreRisque,
        id,
        "Risque soumis pour validation.",
      ),
    valider: (id) =>
      action(
        validerRisque,
        id,
        "Risque validé avec succès.",
      ),
    corriger: (id) =>
      action(
        corrigerRisque,
        id,
        "Risque renvoyé en correction.",
      ),
  };
}