---
title: "Alpha – fonctions en test"
geschuetzt: true
# Kein RSS-Feed (siehe content/fr/mitglieder/_index.md).
outputs: ["html"]
---

Cette page **ne fait pas partie du site public**. On y trouve de nouvelles
fonctions tant qu'elles ne sont pas encore validées – pour les essayer, les
pousser dans leurs retranchements et les évaluer avant qu'elles n'arrivent sur
une vraie page.

Elle est protégée par le même mot de passe que l'espace membres, n'est liée
dans aucun menu, ne figure pas dans le plan du site et n'est pas trouvée par
la recherche. Les moteurs de recherche reçoivent en plus un `noindex`.

*Ce qui figure ici peut disparaître ou changer à tout moment.*

## Générateur d'exercices (apprendre figures et faits)

Tire de nouveaux sets pour « Apprendre des figures » (18 figures) et
« Apprendre des faits » (15 patient·e·s, 18 questions) – séparément ou les deux
ensemble comme le jour du test : d'abord mémoriser les deux, puis la phase
intermédiaire, puis répondre aux deux. Les cases à cocher permettent de choisir
ce qu'on exerce ; les durées s'adaptent au jour du test.

À évaluer : **difficulté et réalisme.** Les figures sont-elles assez
différentes pour être mémorisées en quatre minutes – et les séries se
distinguent-elles assez les unes des autres ? Les noms, professions,
caractéristiques et diagnostics sonnent-ils comme dans un vrai cahier de test,
et les questions sont-elles claires ? En français en particulier : les
accords (« la patiente nerveuse », « l'avocate ») et les tournures des
questions sont-ils corrects ? Et à l'impression : la feuille de réponses et
le corrigé ressemblent-ils à ceux de l'outil de mise en forme ?

```baustein
lern-generator
```

## Évaluer une feuille de réponses

Qui a résolu une simulation de test à la maison sur papier photographie la
feuille de réponses et obtient ses points par sous-test – sans comparer à la
main les 144 solutions. La lecture se fait comme dans l'outil de mise en forme
(évaluation), mais directement dans le navigateur : la photo ne quitte pas
l'appareil. Fonctionne pour les simulations de test 2022 à 2026, qui ont
toutes la même feuille de réponses – et pour chaque simulation de l'outil de
mise en forme : sous « Propre grille de correction », choisir le PDF du corrigé de
l'outil (avec la feuille de réponses dont les bonnes cases sont noircies).
« Caméra en direct » cherche les quatre coins noirs déjà dans le viseur et
déclenche toute seule dès que la feuille est immobile dans l'image ;
« Prendre une photo » ouvre l'appareil photo du téléphone, « Choisir une image
ou un PDF » prend une photo ou un scan existant.

À évaluer surtout : **est-ce que ça marche avec de vraies photos de
téléphone** – de travers, à l'ombre, au crayon, au stylo, avec des croix
gommées ou barrées ? Les croix lues sont-elles correctes ? Les lignes
incertaines (en orange) sont-elles marquées de façon sensée, et faciles à
corriger ? La page lit-elle correctement un test de concentration personnel
de l'outil ? Et : les indications sont-elles compréhensibles quand une photo
ne convient pas ?

```baustein
antwortbogen-auswertung
```

## Évaluer le test de concentration

La même chose pour le test de concentration : photo (ou caméra en direct,
scan, PDF) de la feuille travaillée, comptée selon la règle de la consigne –
marques correctes moins marques fausses moins signes cibles omis avant le
dernier signe marqué. La feuille n'a pas de coins noirs ; c'est la grille des
1600 signes elle-même qui sert de repère (procédé de l'outil de mise en forme).
On peut choisir tous les tests de concentration du site avec corrigé
(simulations de test 2022, 2023, 2026 et séries d'exercices) – ou un test
personnel : télécharger l'exercice et le corrigé en PDF, par exemple depuis
l'outil de mise en forme.

À évaluer : **est-ce que ça marche avec de vraies photos et différents
stylos ?** Les signes barrés, entourés ou à peine touchés sont-ils bien
reconnus ? Une marque mal lue se corrige-t-elle facilement d'un toucher ?

```baustein
konztest-auswertung
```
