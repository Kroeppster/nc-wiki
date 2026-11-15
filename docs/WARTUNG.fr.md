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

## Avant de commencer

**Ce qu'il te faut**

- Un compte gratuit sur [github.com](https://github.com) et une invitation au dépôt
  `Kroeppster/nc-wiki`. L'invitation est donnée par la personne qui s'occupe du site ;
  sans elle, tu peux tout lire, mais rien modifier.
- Pour le classeur : Excel.
- Rien d'autre. Aucun programme à installer, aucune connaissance en programmation.

**Tu ne peux presque rien casser.** GitHub garde pour chaque modification l'état
précédent ; on peut y revenir ([section 12](#12-vérifier-et-annuler)). Si la vérification
automatique trouve une erreur dans ta modification, l'ancien site reste simplement en
ligne.

**Les mots qui reviennent sans cesse**

| Mot | Ce que cela veut dire |
| --- | --- |
| dépôt (repository) | le dossier contenant tous les fichiers du site, sur GitHub |
| `main` | l'état valable. Ce qui est sur `main` est publié |
| commit, « Commit changes » | enregistrer. Chaque modification enregistrée reçoit une courte description, pour que les autres voient ce qui a changé |
| pull request | une proposition de modification, pas encore valable (c'est ainsi qu'arrivent les classeurs) |
| merge | accepter la proposition. Ce n'est qu'ensuite qu'elle est sur `main` |
| construction, « Actions » | après chaque enregistrement, GitHub reconstruit le site et le vérifie. Coche verte : en ligne. Croix rouge : [section 10](#10-quand-la-construction-est-rouge) |
| Markdown, `.md` | de simples fichiers texte à partir desquels les pages sont créées ([section 14](#14-aide-à-la-rédaction)) |
| en-tête de la page | les lignes entre les deux `---` tout en haut d'un fichier `.md` : titre, date, description |

**Les adresses :** site [kroeppster.github.io/nc-wiki](https://kroeppster.github.io/nc-wiki/fr/) ·
fichiers [github.com/Kroeppster/nc-wiki](https://github.com/Kroeppster/nc-wiki) ·
éditeur web [app.pagescms.org](https://app.pagescms.org)

---

## 1. Quel outil pour quoi

| Tu veux … | Outil | Section |
| --- | --- | --- |
| relire beaucoup de textes, traduire, modifier l'accueil ou l'équipe | **classeur Excel** | [2](#2-modifier-les-textes-avec-le-classeur-excel) |
| corriger vite une faute sur une page | **éditeur web** (Pages CMS) | [3](#3-petites-corrections-dans-léditeur-web) |
| écrire une actualité | éditeur web ou GitHub | [4](#4-écrire-une-actualité) |
| téléverser un PDF ou une image, supprimer un fichier | **GitHub** | [5](#5-téléverser-un-pdf) – [8](#8-supprimer-un-fichier-ou-une-page) |
| modifier une page existante directement sur GitHub | **GitHub** | [11](#11-modifier-un-fichier-directement-sur-github) |
| voir si la modification est en ligne, ou annuler quelque chose | **GitHub** | [12](#12-vérifier-et-annuler) |
| changer la date du prochain AMS, passer le site à la nouvelle année | plusieurs | [13](#13-liste-de-contrôle-pour-la-nouvelle-année) |
| savoir comment écrire en gras, faire une liste ou un lien | – | [14](#14-aide-à-la-rédaction) |

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
   classeur, le reste pour toutes les langues. Les noms de colonnes s'écrasent à la ligne 4,
   à droite il y a des colonnes vides pour de nouvelles informations, la ligne 5 détermine
   où une information apparaît.
   **Questions fréquentes – Vue** contient toutes les questions : remplir une ligne vide en bas = nouvelle
   question, `!Supprimer!` dans « Question » = question retirée (dans toutes les langues).
4. **Nouvelle saison :** en haut de la feuille de l'équipe, remplir « Commencer une
   nouvelle saison » (p. ex. 2027/28). L'équipe actuelle passe alors dans les archives,
   dans les trois langues.
5. **Téléverser :** sur GitHub dans le dossier [`redaktion/`](../redaktion/) → *Add file →
   Upload files* → *Commit changes*. Une à deux minutes plus tard, une proposition avec un
   rapport apparaît sous *Pull requests* (ce qui a été repris ou ignoré).
   **Ce n'est en ligne qu'une fois la proposition acceptée (Merge).**
   **Comment accepter la proposition :** en haut, *Pull requests* → cliquer sur la
   nouvelle proposition → lire le rapport. L'onglet *Files changed* montre en rouge ce
   qui disparaît et en vert ce qui s'ajoute. Si tout est juste : retour sur
   *Conversation*, tout en bas **Merge pull request** → **Confirm merge**. Si le rapport
   contient un ❌ (le site ne se construit pas ou la vérification signale quelque
   chose), ne pas encore accepter : corriger d'abord l'endroit indiqué dans un classeur
   récent et le téléverser à nouveau.

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

Deux choses que l'on oublie souvent :

- **Même nom de fichier dans toutes les langues.** L'éditeur web propose le nom de
  fichier à partir du titre, qui diffère d'une langue à l'autre. À la création, saisis le
  même nom dans les trois langues (p. ex. `testsimulation-2027.md`), sinon le choix de
  langue en haut à droite ne mène pas à l'autre version.
- **Une date dans le futur** retient l'article : il n'apparaît que lorsque le jour est
  arrivé et que le site est reconstruit ensuite.

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

**Français et italien :** les fichiers de ces langues vont dans le sous-dossier `fr/` ou
`it/` du dossier concerné (p. ex. `assets/downloads/uebungsaufgaben/muster-zuordnen/fr/`),
avec le même nom. Chaque version linguistique du site n'affiche que les fichiers de sa langue.

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

**Images dans le texte** (p. ex. des captures d'écran dans une actualité) : téléverser
l'image aussi dans `assets/images/<rubrique>/` et l'insérer dans le texte, sur une ligne
à part :

```markdown
![Ce que montre l'image](news/neue-website/fr/uniguide.png "Légende")
```

La description entre crochets est obligatoire, la légende entre guillemets facultative.
Ici aussi, le chemin commence **après** `assets/images/`. S'il est faux, la construction
échoue avec un message.

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
| « Check built site » | une page sans titre, description ou titre principal, une adresse sans `/nc-wiki/` ou un texte de l'espace membres visible sans protection | le message indique le type et le fichier ; corriger dans le fichier indiqué |
| « Build with Hugo » | erreur dans l'en-tête (guillemets, indentation, description d'image manquante) | comparer avec un fichier qui fonctionne |

Les liens vers d'autres sites sont vérifiés une fois par semaine par un déroulement à
part (« Externe Links prüfen ») ; s'il est rouge, un tel lien est cassé, le site
lui-même fonctionne normalement. De même « Prüfstand » (chaque nuit) : il parcourt le
site dans un navigateur et n'y change rien. Si tu es bloqué·e :
sous *Issues → New issue*, poster le lien vers l'exécution rouge.

Pour une pull request, la même vérification tourne déjà avant l'acceptation – un ✗ rouge
signifie : ne pas encore fusionner.

---

## 11. Modifier un fichier directement sur GitHub

Pour tout ce que l'éditeur web ne propose pas, ou si tu préfères travailler sur GitHub.

1. Ouvrir [github.com/Kroeppster/nc-wiki](https://github.com/Kroeppster/nc-wiki) et se
   connecter.
2. **Trouver le fichier.** Les pages se trouvent sous `content/fr/` (allemand :
   `content/de/`, italien : `content/it/`), organisées comme les adresses du site :

   | Adresse de la page | Fichier |
   | --- | --- |
   | `…/nc-wiki/fr/impressum/` | `content/fr/impressum.md` |
   | `…/nc-wiki/fr/ems/` | `content/fr/ems/_index.md` (page d'ensemble d'un dossier) |
   | `…/nc-wiki/ems/uniguide/` | `content/de/ems/uniguide/_index.md` |

   Plus rapide : taper une partie du nom dans le champ *Go to file*, en haut.
3. Cliquer sur le fichier → en haut à droite, l'**icône du crayon** (*Edit this file*).
4. Modifier le texte. Dans l'en-tête (entre les `---`), ne changer que ce qui est entre
   guillemets ; les mots avant les deux-points et le retrait restent.
5. En haut à droite **Commit changes…** → décrire en une phrase ce que tu as changé →
   **Commit changes**.
6. Attendre une à deux minutes et recharger la page
   ([section 12](#12-vérifier-et-annuler)).

---

## 12. Vérifier et annuler

**Ma modification est-elle en ligne ?** Sur GitHub, en haut, **Actions**. Le déroulement
le plus récent « Deploy Hugo site to GitHub Pages » indique l'état :

| Signe | Signification |
| --- | --- |
| cercle jaune | la construction est en cours (environ deux minutes) |
| coche verte | terminé, la modification est en ligne |
| croix rouge | une erreur, la modification n'est **pas** en ligne ([section 10](#10-quand-la-construction-est-rouge)) |

Recharger ensuite la page dans le navigateur, de préférence sans le cache : Ctrl+F5
(Windows) ou Cmd+Shift+R (Mac).

**La modification n'apparaît pas ?** Vérifier dans l'ordre :

1. La construction est-elle verte ? (voir ci-dessus)
2. Classeur téléversé : la proposition sous *Pull requests* a-t-elle déjà été acceptée ?
3. L'en-tête contient-il `draft: true`, ou la date est-elle dans le futur ? La page reste
   alors cachée.
4. Regardes-tu la bonne langue ? Une modification sous `content/fr/` ne se voit que sur
   la page française.
5. Le fichier est-il dans le bon dossier et se termine-t-il par `.md` ?

**Annuler quelque chose**

- **Un classeur accepté (pull request) :** *Pull requests* → *Closed* → ouvrir la
  proposition → en bas **Revert** → une nouvelle proposition est créée, qui annule tout →
  l'accepter (Merge).
- **Un seul fichier :** ouvrir le fichier → en haut à droite **History**. Chaque version y
  figure avec sa date et sa description. Cliquer sur la version qui était encore juste →
  en haut à droite **…** → *View file* → copier le texte. Retour au fichier actuel,
  icône du crayon, tout remplacer par le texte copié, **Commit changes**.
- **Un fichier supprimé, ou si tu n'es pas sûr·e :** décrire ce qui s'est passé sous
  *Issues → New issue*. Rien n'est perdu ; quelqu'un de plus expérimenté le récupère.

---

## 13. Liste de contrôle pour la nouvelle année

Une fois par an, dès que la date du prochain AMS est connue.

| Quoi | Où | Comment |
| --- | --- | --- |
| date du prochain AMS (compte à rebours de l'accueil) | fichier `hugo.toml`, ligne `ems_exam_date` | comme à la [section 11](#11-modifier-un-fichier-directement-sur-github) : ne changer que la date entre les guillemets. Forme : `2027-07-09T08:00:00+02:00` signifie 9 juillet 2027, 8 h, heure d'été suisse. Le texte au-dessus du compte à rebours reprend la date tout seul |
| dates de la frise de l'accueil | classeur, feuille de l'accueil (vue) | [section 2](#2-modifier-les-textes-avec-le-classeur-excel) |
| date dans les questions fréquentes | classeur, feuille des questions fréquentes (vue) | section 2 |
| date sur la page « AMS » | éditeur web, page « AMS » | [section 3](#3-petites-corrections-dans-léditeur-web) |
| délais et « état » dans l'Uniguide | classeur, feuille de l'Uniguide (vue) | section 2 ; n'inscrire que ce qui figure sur une page officielle |
| nouvelle saison de l'équipe | classeur, feuille de l'équipe (vue), « Commencer une nouvelle saison » | section 2 |
| nouvelle simulation de test, nouvelles séries d'exercices | téléverser les PDF | [section 5](#5-téléverser-un-pdf) |
| solutions pour « évaluer la feuille de réponses » et « évaluer le test de concentration » | demande quelqu'un avec des connaissances techniques | [guide détaillé, section 11](WARTUNG-DETAILLIERT.fr.md) |

Pour finir, chercher l'ancienne année sur le site avec la loupe : ce qui apparaît encore
et n'est pas une rétrospective a été oublié.

---

## 14. Aide à la rédaction

Voici comment écrire dans un fichier `.md` et dans la colonne « Texte » du classeur.
Dans l'éditeur web, il y a des boutons pour cela.

| Tu veux | Tu écris |
| --- | --- |
| un intertitre | `## Titre` (plus petit : `### Titre`). Jamais un seul `#`, le titre de la page est déjà le titre principal |
| du gras | `**important**` |
| une liste à puces | chaque ligne commence par `- ` |
| une liste numérotée | chaque ligne commence par `1. `, `2. ` … |
| un nouveau paragraphe | une ligne vide entre les deux |
| un lien vers une page du site | `[Uniguide](/ems/uniguide)` ([section 9](#9-liens-et-blocs-dans-le-texte)) |
| un lien vers un autre site | `[swissuniversities](https://www.swissuniversities.ch/)` |
| un astérisque visible (p. ex. l'étoile de genre dans un texte allemand) | `Tutor\*innen`, avec une barre oblique inversée devant l'étoile. Sans elle, Markdown met en italique ce qui se trouve entre deux étoiles d'un même paragraphe, et la construction s'arrête avec un message. Dans l'éditeur web, taper simplement `*` |
| des guillemets | « ainsi », pas "ainsi" |

La manière d'écrire (tutoiement, termes, date « 9 juillet 2027 ») est décrite dans le
[guide de style](STYLEGUIDE.md) (en allemand).

---

## 15. Les règles essentielles

- **Tout en trois langues.** Les nouveaux textes visibles toujours en allemand, français
  et italien.
- **Même nom de fichier dans toutes les langues.** C'est ainsi seulement que le choix de
  langue trouve les autres versions d'une page.
- **Le dépôt est public.** Pas de mots de passe, données personnelles ou notes internes
  dans les fichiers ou les classeurs. Les accès vont dans le gestionnaire de mots de passe
  de l'association.
- **Ne pas inventer de chiffres.** Dans l'Uniguide, n'inscrire que ce qui figure sur une
  page officielle ; les nombres de l'accueil sont comptés par le site lui-même.
- **La mention de licence reste.** Les exercices sont sous licence CC BY-NC 4.0 ; la
  mention n'est pas retirée.
- **En cas de doute, demander** avant de modifier quoi que ce soit dans `layouts/`,
  `.github/` ou `hugo.toml`.
