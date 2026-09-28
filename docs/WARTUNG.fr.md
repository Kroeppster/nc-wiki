# Entretenir le site – guide rapide

[Deutsch](WARTUNG.md) · **Français** · [Italiano](WARTUNG.it.md)

Ce guide ne contient que le quotidien : modifier des textes, écrire une actualité,
téléverser des PDF et des images, supprimer quelque chose. Tout se fait dans le
navigateur, rien à installer. Tout le reste (page d'accueil, équipe, menu, design,
formulaires, espace membres, technique) se trouve dans le
**[guide détaillé](WARTUNG-DETAILLIERT.fr.md)**.

Les noms de fichiers et de dossiers (`content/de/…`, `redaktion/` …) restent en allemand,
car ce sont les vrais noms dans le dépôt.

---

## 1. Quel outil pour quoi

| Tu veux … | Outil | Section |
| --- | --- | --- |
| relire beaucoup de textes, traduire, modifier l'accueil ou l'équipe | **classeur Excel** | [2](#2-modifier-les-textes-avec-le-classeur-excel) |
| corriger vite une faute sur une page | **éditeur web** (Pages CMS) | [3](#3-petites-corrections-dans-léditeur-web) |
| écrire une actualité | éditeur web ou GitHub | [4](#4-écrire-une-actualité) |
| téléverser un PDF ou une image, supprimer un fichier | **GitHub** | [5](#5-téléverser-un-pdf) – [8](#8-supprimer-un-fichier-ou-une-page) |

Tous les outils modifient les mêmes fichiers. Après chaque modification sur `main`,
GitHub reconstruit le site ; il est en ligne une à deux minutes plus tard.

---

## 2. Modifier les textes avec le classeur Excel

Il y a **un classeur par langue** (DE, FR, IT) avec tous les textes visibles du site –
chaque page sur sa propre feuille, avec au début un mode d'emploi et une table des
matières.

1. **Prendre un classeur récent :** sur GitHub, à droite sous *Releases → Textmappen*, ou
   directement :
   [DE](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-de.xlsx) ·
   [FR](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-fr.xlsx) ·
   [IT](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-it.xlsx).
   Il est regénéré automatiquement après chaque modification. **Toujours commencer avec un
   classeur récent.**
2. **Travailler dans les cellules :**

   | Quoi | Comment |
   | --- | --- |
   | Modifier un texte | écraser le texte dans la colonne « Texte » (devient jaune) |
   | Nouveau paragraphe | dans la même cellule, après une ligne vide (deux fois Alt+Entrée, Mac : Ctrl+Option+Entrée) |
   | Nouvelle ligne / titre | insérer une **ligne entière** (numéro de ligne → clic droit → Insérer), choisir la sorte dans « Type » (devient verte) |
   | Supprimer un paragraphe | `!Supprimer!` dans la cellule (devient rouge) |
   | Supprimer une page entière | `!Supprimer!` dans la ligne grise « Page » |
   | Changer l'ordre | couper la ligne entière et l'insérer au nouvel endroit |

   Toujours insérer ou déplacer des **lignes entières**, jamais des cellules isolées. Une
   cellule vide ne supprime rien – seul `!Supprimer!` supprime.
3. **L'accueil et l'équipe** ont chacun une feuille « … – Vue » (onglet orange), construite
   comme le site. N'écrire que dans les cases blanches. Équipe : remplir une carte vide =
   nouvelle personne, `!Supprimer!` dans le nom = personne retirée.
   **Uniguide – Vue** contient tout le tableau des universités : une ligne par université,
   une colonne par information. Les textes (en-têtes verts) valent pour la langue du
   classeur, le reste pour toutes les langues.
4. **Nouvelle saison :** en haut de la feuille de l'équipe, remplir « Commencer une
   nouvelle saison » (p. ex. 2027/28). L'équipe actuelle passe alors dans les archives,
   dans les trois langues.
5. **Téléverser :** sur GitHub dans le dossier [`redaktion/`](../redaktion/) → *Add file →
   Upload files* → *Commit changes*. Une à deux minutes plus tard, une proposition avec un
   rapport apparaît sous *Pull requests* (ce qui a été repris ou ignoré).
   **Ce n'est en ligne qu'une fois la proposition acceptée (Merge).**

Le classeur français montre le texte allemand comme modèle à côté ; les traductions
manquantes sont des lignes vides qu'il suffit de remplir. L'équipe en français se gère dans
le classeur français.

> **Le dépôt est public.** Tout ce qui figure dans un classeur téléversé – remarques
> comprises – reste lisible par tout le monde.

Plus de détails (ce qui se passe exactement à la lecture, cas d'erreur) : guide détaillé,
[section 3](WARTUNG-DETAILLIERT.fr.md#3-classeurs-excel-en-détail).

---

## 3. Petites corrections dans l'éditeur web

**[app.pagescms.org](https://app.pagescms.org)** – se connecter avec GitHub ou via l'e-mail
d'invitation, ouvrir le dépôt `Kroeppster/nc-wiki`. À gauche, choisir la langue puis les
pages, actualités ou témoignages, modifier le texte comme dans un traitement de texte et
cliquer sur **Save**. C'est aussitôt une modification sur `main`, en ligne une à deux
minutes plus tard.

Trois règles :

- Laisser les cases grises `baustein` (équipe, déroulement du test, générateurs …) telles
  quelles, ne rien écrire dedans.
- Liens vers nos propres pages uniquement avec le chemin, p. ex. `/ems/uniguide` (voir
  [section 9](#9-liens-et-blocs-dans-le-texte)).
- Ne pas renommer ni supprimer de pages dans l'éditeur, mais sur GitHub
  ([section 8](#8-supprimer-un-fichier-ou-une-page)).

L'accueil (frise, tuiles) et l'équipe se gèrent plutôt avec le classeur Excel.

---

## 4. Écrire une actualité

**Dans l'éditeur web :** *News* de la langue voulue → créer une nouvelle entrée → remplir
titre, date, mot-clé (p. ex. « Mise à jour ») et texte → **Save**.

**Sur GitHub :** dans `content/fr/news/`, créer un nouveau fichier `mon-titre.md` (*Add
file → Create new file*). Un modèle à copier se trouve dans
[`docs/vorlage-news.md`](vorlage-news.md) (en allemand).

Les premières phrases apparaissent automatiquement comme aperçu dans la liste des
actualités et sur l'accueil. Tant que `draft: true` figure dans l'en-tête, l'article reste
invisible. Créer le même article en allemand et en italien (même nom de fichier sous
`content/de/news/` et `content/it/news/`).

---

## 5. Téléverser un PDF

**Série d'exercices, simulation de test, script de cours** – il suffit de le téléverser
dans le bon dossier, il apparaît automatiquement sur le site :

| Matériel | Dossier |
| --- | --- |
| Séries d'exercices | `assets/downloads/uebungsaufgaben/<sous-test>/` (les sous-dossiers existent déjà) |
| Simulations de test | `assets/downloads/testsimulationen/` |
| Scripts de cours | `assets/downloads/kursskripte/` |
| Espace membres | `assets/downloads/mitglieder/` |

Sur GitHub, aller dans le dossier → *Add file → Upload files* → glisser le PDF → *Commit
changes*. Les séries s'appellent `<année>_<nom-du-dossier>_S<numéro>.pdf`, p. ex.
`2027_muster-zuordnen_S02.pdf` ; la solution porte le même nom avec `_Loesung` à la fin. Le
nom affiché sur le site en est tiré automatiquement.

**Rapport annuel et autres documents isolés** : ils ont besoin d'une page à eux – voir le
guide détaillé, [section 2](WARTUNG-DETAILLIERT.fr.md#2-pages-menu-et-navigation).

---

## 6. Ajouter une image

Chaque page peut avoir **une** image de titre (en haut de la page et comme aperçu dans les
listes).

1. Téléverser l'image dans `assets/images/<rubrique>/`, p. ex.
   `assets/images/news/simulation-2027.jpg`.
2. Ajouter dans l'en-tête de la page :

   ```yaml
   featured_image: "news/simulation-2027.jpg"
   featured_image_alt: "Brève description de ce que montre l'image"
   ```

   Le chemin commence **après** `assets/images/`. La description est obligatoire (pour
   les personnes utilisant un lecteur d'écran) ; sans elle, la construction échoue.

Les grandes images ne posent pas de problème – le site les réduit lui-même.

---

## 7. Créer une nouvelle page

1. Sur GitHub, aller dans le dossier voulu sous `content/fr/` → *Add file → Create new
   file*.
2. Nom du fichier : en minuscules, sans accents ni espaces, se termine par `.md`
   (p. ex. `nouvelle-page.md`). Il fait partie de l'adresse – il doit être **identique**
   dans les trois langues.
3. Contenu :

   ```markdown
   ---
   title: "Titre de la page"
   description: "Une phrase qui apparaît dans Google sous le titre (160 caractères max.)."
   ---

   Texte de la page.
   ```

4. Créer le même fichier, traduit, sous `content/de/` et `content/it/`.

Pour que la page apparaisse dans le menu : guide détaillé,
[section 2](WARTUNG-DETAILLIERT.fr.md#2-pages-menu-et-navigation).

---

## 8. Supprimer un fichier ou une page

Ouvrir le fichier sur GitHub → en haut à droite **…** → *Delete file* → *Commit changes*.

- Supprimer une page dans **les trois langues**.
- Pour les séries d'exercices, supprimer l'exercice **et** le fichier `_Loesung`.
- Si un lien pointe encore vers la page supprimée, la construction devient rouge et
  indique l'endroit – y retirer le lien.

---

## 9. Liens et blocs dans le texte

**Liens internes** : un lien normal avec le chemin, sans la langue :

```markdown
Plus d'infos dans l'[Uniguide](/ems/uniguide).
```

Sur la page française, il devient automatiquement le lien vers la page française. Si la
page cible n'existe pas, la construction s'arrête avec un message – ainsi aucun lien mort
n'est mis en ligne.

**Blocs** (cartes de l'équipe, tableau du déroulement, générateurs, contact sponsoring) :
une case grise dans le texte :

````markdown
```baustein
team-leitung
```
````

On peut les déplacer, mais pas écrire dedans. Ne jamais écrire de `{{< … >}}` dans le
texte – l'éditeur web les détruit.

---

## 10. Quand la construction est rouge

**Le site reste en ligne** – seule la dernière modification manque jusqu'à la correction.

1. Sur GitHub, en haut **Actions** → ouvrir la dernière exécution avec ✗ rouge → job
   **build**.
2. Déplier l'étape marquée ✗ ; le fichier concerné y est généralement indiqué.

| Rouge à | Le plus souvent | Que faire |
| --- | --- | --- |
| « Check internal links », ou « Build with Hugo » avec « Link » | un lien pointe dans le vide | corriger le lien dans le fichier indiqué |
| « Build with Hugo » | erreur dans l'en-tête (guillemets, indentation, description d'image manquante) | comparer avec un fichier qui fonctionne |

« Check external links » n'est qu'un avertissement et ne casse rien. Si tu es bloqué·e :
sous *Issues → New issue*, poster le lien vers l'exécution rouge.

Pour une pull request, la même vérification tourne déjà avant l'acceptation – un ✗ rouge
signifie : ne pas encore fusionner.

---

## 11. Les règles essentielles

- **Tout en trois langues.** Les nouveaux textes visibles toujours en allemand, français
  et italien.
- **Le dépôt est public.** Pas de mots de passe, données personnelles ou notes internes
  dans les fichiers ou les classeurs. Les accès vont dans le gestionnaire de mots de passe
  de l'association.
- **Ne pas inventer de chiffres.** Dans l'Uniguide, n'inscrire que ce qui figure sur une
  page officielle ; les nombres de l'accueil sont comptés par le site lui-même.
- **La mention de licence reste.** Les exercices sont sous licence CC BY-NC 4.0 ; la
  mention n'est pas retirée.
- **En cas de doute, demander** avant de modifier quoi que ce soit dans `layouts/`,
  `.github/` ou `hugo.toml`.
