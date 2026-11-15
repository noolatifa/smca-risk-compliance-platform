import { useCallback, useEffect, useState } from "react";

import {
  corrigerBia,
  creerBia,
  listerActivites,
  listerBias,
  modifierBia,
  soumettreBia,
  validerBia,
} from "../services/biaService";

const IMPACT_VIDE = {
  horizon_heures: 1,
  clients: "",
  operations: "",
  finances: "",
  engagements: "",
  reputation: "",
};

function creerFormulaireVide() {
  return {
    activite_id: "",
    responsable: "",
    heures_fonctionnement: "",
    sites_concernes: "",
    periode_pointe: "",
    mtpd_heures: "",
    justification_mtpd: "",
    rto_heures: "",
    capacite_minimale_pct: "",
    rpo_heures: "",
    justification_rpo: "",
    statut: "brouillon",
    impacts: [{ ...IMPACT_VIDE }],
  };
}

function convertirBiaVersFormulaire(bia) {
  return {
    activite_id: String(bia.activite_id),
    responsable: bia.responsable || "",
    heures_fonctionnement: bia.heures_fonctionnement || "",
    sites_concernes: bia.sites_concernes || "",
    periode_pointe: bia.periode_pointe || "",
    mtpd_heures: bia.mtpd_heures ?? "",
    justification_mtpd: bia.justification_mtpd || "",
    rto_heures: bia.rto_heures ?? "",
    capacite_minimale_pct: bia.capacite_minimale_pct ?? "",
    rpo_heures: bia.rpo_heures ?? "",
    justification_rpo: bia.justification_rpo || "",
    statut: bia.statut,
    impacts:
      bia.impacts?.length > 0
        ? bia.impacts.map((impact) => ({
            horizon_heures: impact.horizon_heures,
            clients: impact.clients || "",
            operations: impact.operations || "",
            finances: impact.finances || "",
            engagements: impact.engagements || "",
            reputation: impact.reputation || "",
          }))
        : [{ ...IMPACT_VIDE }],
  };
}

function convertirFormulairePourApi(formulaire) {
  const resultat = {
    activite_id: Number(formulaire.activite_id),
    responsable: formulaire.responsable || null,
    heures_fonctionnement:
      formulaire.heures_fonctionnement || null,
    sites_concernes: formulaire.sites_concernes || null,
    periode_pointe: formularioValue(formulaire.periode_pointe),
    mtpd_heures: nombreOuNull(formulaire.mtpd_heures),
    justification_mtpd:
      formularioValue(formulaire.justification_mtpd),
    rto_heures: nombreOuNull(formulaire.rto_heures),
    capacite_minimale_pct: nombreOuNull(
      formulaire.capacite_minimale_pct,
    ),
    rpo_heures: nombreOuNull(formulaire.rpo_heures),
    justification_rpo:
      formularioValue(formulaire.justification_rpo),
    impacts: formulaire.impacts.map((impact) => ({
      horizon_heures: Number(impact.horizon_heures),
      clients: impact.clients || null,
      operations: impact.operations || null,
      finances: impact.finances || null,
      engagements: impact.engagements || null,
      reputation: impact.reputation || null,
    })),
  };

  return resultat;
}

function formularioValue(value) {
  return value || null;
}

function nombreOuNull(value) {
  return value === "" || value === null ? null : Number(value);
}

export function useBia() {
  const [bias, setBias] = useState([]);
  const [activites, setActivites] = useState([]);
  const [formulaire, setFormulaire] = useState(creerFormulaireVide());
  const [biaSelectionnee, setBiaSelectionnee] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState("");
  const [message, setMessage] = useState("");

  const chargerDonnees = useCallback(async () => {
    try {
      setChargement(true);
      setErreur("");

      const [biasData, activitesData] = await Promise.all([
        listerBias(),
        listerActivites(),
      ]);

      setBias(biasData);
      setActivites(activitesData);
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

  function modifierImpact(index, event) {
    const { name, value } = event.target;

    setFormulaire((ancien) => ({
      ...ancien,
      impacts: ancien.impacts.map((impact, impactIndex) =>
        impactIndex === index
          ? { ...impact, [name]: value }
          : impact,
      ),
    }));
  }

  function ajouterImpact() {
    const horizonsUtilises = formulaire.impacts.map((impact) =>
      Number(impact.horizon_heures),
    );

    const horizonDisponible = [1, 4, 8, 24, 72].find(
      (horizon) => !horizonsUtilises.includes(horizon),
    );

    if (!horizonDisponible) {
      setErreur("Tous les horizons disponibles sont déjà utilisés.");
      return;
    }

    setFormulaire((ancien) => ({
      ...ancien,
      impacts: [
        ...ancien.impacts,
        {
          ...IMPACT_VIDE,
          horizon_heures: horizonDisponible,
        },
      ],
    }));
  }

  function supprimerImpact(index) {
    setFormulaire((ancien) => ({
      ...ancien,
      impacts: ancien.impacts.filter(
        (_, impactIndex) => impactIndex !== index,
      ),
    }));
  }

  function reinitialiserFormulaire() {
    setBiaSelectionnee(null);
    setFormulaire(creerFormulaireVide());
    setErreur("");
    setMessage("");
  }

  function selectionnerBia(bia) {
    setBiaSelectionnee(bia);
    setFormulaire(convertirBiaVersFormulaire(bia));
    setErreur("");
    setMessage("");
  }

  async function enregistrerBia(event) {
    event.preventDefault();

    try {
      setErreur("");
      setMessage("");

      const donnees = convertirFormulairePourApi(formulaire);

      if (biaSelectionnee) {
        await modifierBia(biaSelectionnee.id, {
          responsable: donnees.responsable,
          heures_fonctionnement: donnees.heures_fonctionnement,
          sites_concernes: donnees.sites_concernes,
          periode_pointe: donnees.periode_pointe,
          mtpd_heures: donnees.mtpd_heures,
          justification_mtpd: donnees.justification_mtpd,
          rto_heures: donnees.rto_heures,
          capacite_minimale_pct: donnees.capacite_minimale_pct,
          rpo_heures: donnees.rpo_heures,
          justification_rpo: donnees.justification_rpo,
          impacts: donnees.impacts,
        });

        setMessage("BIA modifiée avec succès.");
      } else {
        await creerBia({
          ...donnees,
          statut: "brouillon",
        });

        setMessage("BIA créée avec succès.");
      }

      await chargerDonnees();
      reinitialiserFormulaire();
    } catch (error) {
      setErreur(error.message);
    }
  }

  async function executerAction(action, id, texte) {
    try {
      setErreur("");
      setMessage("");

      await action(id);

      setMessage(texte);
      await chargerDonnees();

      const nouvelleBia = (await listerBias()).find(
        (bia) => bia.id === id,
      );

      if (nouvelleBia) {
        selectionnerBia(nouvelleBia);
      }
    } catch (error) {
      setErreur(error.message);
    }
  }

  return {
    bias,
    activites,
    formulaire,
    biaSelectionnee,
    chargement,
    erreur,
    message,
    modifierChamp,
    modifierImpact,
    ajouterImpact,
    supprimerImpact,
    selectionnerBia,
    reinitialiserFormulaire,
    enregistrerBia,
    chargerDonnees,
    soumettre: (id) =>
      executerAction(
        soumettreBia,
        id,
        "BIA soumise pour validation.",
      ),
    valider: (id) =>
      executerAction(
        validerBia,
        id,
        "BIA validée avec succès.",
      ),
    corriger: (id) =>
      executerAction(
        corrigerBia,
        id,
        "BIA renvoyée en correction.",
      ),
  };
}