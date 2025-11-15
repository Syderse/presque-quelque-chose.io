---
title: "ÉTALON V2 : RAPPORT DE CALIBRAGE DES COULEURS ET POLICES"
date: 2025-11-15
summary: "Ceci est le test v2 pour vérifier la solution radicale. il teste à la fois les variables css (pour les composants) et les classes tailwind (pour le contenu)."
---

---
title: "Spécimen de Style 'Pataphysique"
date: 2025-11-15
summary: "Une page de test pour valider tous les éléments de style CSS personnalisés."
---

Ceci est une page de test 'pataphysique. Elle contient tous les éléments Markdown que nous avons ciblés. Si la configuration est correcte, chaque élément ci-dessous devrait avoir un style distinct.

---

## 1. Test de Typographie (Polices)

Ce paragraphe est en texte de corps normal.

> **Résultat Attendu :** Le texte ci-dessus doit être en police **EB Garamond** (une police *serif* classique).

### Ceci est un Titre de Niveau 3

> **Résultat Attendu :** Le titre ci-dessus doit être en police **Playfair Display** (une police *serif* plus décorative) ET avoir un **dégradé de bleu**.

Et ceci est du `code inline`.

> **Résultat Attendu :** Le code `inline` ci-dessus doit être en police **Special Elite** (un style *machine à écrire*).

---

## 2. Test des Styles Markdown (Couleurs)

*Ceci est du texte en italique.*

> **Résultat Attendu :** Le texte en italique doit être **VERT** (`#008000`).

**Ceci est du texte en gras.**

> **Résultat Attendu :** Le texte en gras doit être **BLANC LUMINEUX**. (Note : il sera presque invisible si le fond de votre page est blanc. C'est le style que vous avez demandé.)

***Ceci est en gras et italique.***

> **Résultat Attendu :** Ce texte doit être **VIOLET** (`#EE82EE`).

---

## 3. Test des Blocs (Couleurs)

> "La 'pataphysique est la science des solutions imaginaires."
> — Alfred Jarry

> **Résultat Attendu :** Le bloc de citation ci-dessus doit avoir une **bordure gauche orange vif**, un **fond orange très clair**, et le **texte lui-même doit être d'un orange plus foncé** (`#E67E22`).

```javascript
// Ceci est un bloc de code
function laGidouille() {
  return "Ubu Roi";
}