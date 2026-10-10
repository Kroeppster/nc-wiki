# Entretenir le site – guide détaillé

[Deutsch](WARTUNG-DETAILLIERT.md) · **Français** · [Italiano](WARTUNG-DETAILLIERT.it.md)

Les tâches quotidiennes (textes, actualités, PDF, images, suppression) se trouvent dans le
**[guide rapide](WARTUNG.fr.md)**. Ici figure tout le reste – du menu à l'accueil, l'équipe
et le design jusqu'à la technique. La plupart des sections se font dans le navigateur sur
github.com ; quand il faut son propre ordinateur ou des connaissances en programmation,
c'est indiqué.

Les noms de fichiers, de dossiers et de champs restent en allemand, car ce sont les vrais
noms dans le dépôt.

## Sommaire

1. [Structure du projet](#1-structure-du-projet)
2. [Pages, menu et navigation](#2-pages-menu-et-navigation)
3. [Classeurs Excel en détail](#3-classeurs-excel-en-détail)
4. [Éditeur web (Pages CMS) en détail](#4-éditeur-web-pages-cms-en-détail)
5. [Liens, blocs et contenus programmés](#5-liens-blocs-et-contenus-programmés)
6. [Page d'accueil](#6-page-daccueil)
7. [Équipe et nouvelle saison](#7-équipe-et-nouvelle-saison)
8. [Soutien, dons, sponsors](#8-soutien-dons-sponsors)
9. [FAQ, Uniguide, sous-tests, noms de téléchargement](#9-faq-uniguide-sous-tests-noms-de-téléchargement)
10. [Mode examen](#10-mode-examen)
11. [Générateurs d'apprentissage et page Alpha](#11-générateurs-dapprentissage-et-page-alpha)
12. [Espace membres](#12-espace-membres)
13. [Formulaires](#13-formulaires)
14. [Réglages dans hugo.toml](#14-réglages-dans-hugotoml)
15. [Textes fixes (i18n)](#15-textes-fixes-i18n)
16. [Design : couleurs, police, logo, liste des sections](#16-design--couleurs-police-logo-liste-des-sections)
17. [Supprimer toute une rubrique](#17-supprimer-toute-une-rubrique)
18. [Automatisations (GitHub Actions)](#18-automatisations-github-actions)
19. [Vérifier le site](#19-vérifier-le-site)
20. [Services tiers et accès](#20-services-tiers-et-accès)
21. [Où s'arrête le simple remplissage ?](#21-où-sarrête-le-simple-remplissage-)

---

## 1. Structure du projet

Le site est construit avec [Hugo](https://gohugo.io/) à partir de fichiers texte. Chaque
modification sur `main` déclenche une construction ; une à deux minutes plus tard, la
nouvelle version est en ligne sur GitHub Pages (`kroeppster.github.io/nc-wiki/`).

| Dossier / fichier | Contenu | À toucher ? |
| --- | --- | --- |
| `content/de\|fr\|it/` | toutes les pages, même structure par langue | constamment |
| `data/*.yaml` | listes : FAQ, universités, sous-tests, déroulement du test, sponsors, noms de téléchargement, contact dons/sponsoring, listes de mots | parfois |
| `assets/downloads/` | PDF listés automatiquement | lors d'un téléversement |
| `assets/images/`, `static/images/` | images (titres, logos) ou logo et graphiques fixes | parfois |
| `i18n/de\|fr\|it.yaml` | textes fixes (boutons, formulaires, annonces) | rarement |
| `hugo.toml` | réglages (compte à rebours, Analytics, réseaux sociaux) | rarement |
| `layouts/`, `assets/css/` | apparence et logique | seulement avec des connaissances |
| `.github/workflows/` | automatisations | seulement avec des connaissances |
| `redaktion/` | dépôt pour les classeurs téléversés | lors d'un téléversement |
| `scripts/` | outils (classeurs, vérifications, images) | seulement avec des connaissances |
| `archetypes/`, `docs/vorlage-*.md` | modèles à copier | comme aide |

Dans chaque dossier sous `content/`, **`_index.md`** est la page d'aperçu du dossier ; tout
autre fichier `.md` est une page individuelle. Une nouvelle rubrique a toujours besoin
d'abord d'un `_index.md` – sans lui, le dossier n'existe pas pour Hugo.

Chaque fichier commence par un **en-tête** entre deux lignes `---` (titre, description,
menu, date …), suivi du texte en Markdown (`**gras**`, `[lien](/chemin)`, `- ` pour les
listes, `## ` pour les intertitres).

**Travailler en local** (facultatif) : installer Hugo Extended (version dans
`.github/workflows/hugo.yml`), puis `npm install` et `hugo server -D` – le site tourne sur
http://localhost:1313/. `npm run build` construit comme sur GitHub.

---

## 2. Pages, menu et navigation

### Champs importants de l'en-tête

| Champ | Effet |
| --- | --- |
| `title` | titre de la page |
| `description` | texte sous le titre dans Google ; ~160 caractères max. |
| `draft: true` | la page n'est pas publiée |
| `date` | actualités et rapports annuels : tri |
| `featured_image`, `featured_image_alt` | image de titre, voir guide rapide 6 |
| `menu` | entrée de menu, voir ci-dessous |
| `aliases` | anciennes adresses qui redirigent ici |
| `downloads` | liste de PDF propre (rapports annuels) |
| `download_ordner` | liste de PDF automatique à partir d'un dossier sous `assets/` |
| `leer_hinweis: true` | la page de liste affiche une note tant qu'il n'y a pas encore de sous-pages (rapports annuels) |
| `geschuetzt: true` | protection par mot de passe, voir [12](#12-espace-membres) |
| `layout` | modèle particulier, p. ex. `spenden` |

### Le menu

Le menu principal est composé **uniquement à partir des en-têtes** – il n'existe pas de
fichier de menu. Premier niveau aujourd'hui : Accueil, Actualités, EMS, Nos soutiens, À
propos de nous, Contact.

```yaml
menu:
  main:
    parent: ueber-uns   # sous quelle entrée
    weight: 5           # ordre, plus petit = plus en avant
    name: "Nom court"   # facultatif, sinon le title
```

- `parent` est le nom du dossier de la rubrique parente (`ems`, `ueber-uns`,
  `unterstuetzer-innen`) ; sans `parent`, la page devient une entrée de premier niveau.
- `weight` peut être décimal (`2.5`) pour glisser une entrée entre deux autres.
- Le bloc de menu doit figurer dans **chaque version linguistique**.
- Le pied de page a son propre menu `legal` (mentions légales, protection des données …),
  construit de la même façon.
- Les sous-menus s'ouvrent à la souris et au toucher ; sur mobile seulement au toucher.
  Rien à régler.

### Renommer ou déplacer une page

L'adresse change aussi. Pour que les anciens liens fonctionnent encore, au **nouvel**
emplacement :

```yaml
aliases:
  - /ancien/chemin/
```

Les liens internes au site pointent dans le vide tant qu'ils ne sont pas adaptés – la
construction indique chaque endroit.

### Rapport annuel et autres documents isolés

1. Téléverser le PDF dans `static/downloads/jahresberichte/2027.pdf`.
2. Nouvelle page `content/fr/ueber-uns/jahresberichte/2027.md` (modèle :
   `archetypes/jahresbericht.md`) :

   ```yaml
   ---
   title: "Rapport annuel 2027"
   date: 2027-01-01
   downloads:
     - path: "downloads/jahresberichte/2027.pdf"   # relatif à static/
       label: "Rapport annuel 2027 (PDF)"
   ---
   Deux ou trois phrases sur l'année.
   ```

   La taille du fichier est ajoutée automatiquement. Idem en DE et IT.

### Listes de PDF automatiques

`download_ordner: "downloads/mitglieder"` dans l'en-tête liste tous les PDF de
`assets/downloads/mitglieder/`. Exercices, simulations et scripts de cours ont leurs
listes intégrées. Pour un nom d'affichage plus joli que le nom de fichier :
`data/downloads.yaml` (le format y est expliqué, avec traductions).

---

## 3. Classeurs Excel en détail

Déroulement pour la rédaction : [guide rapide 2](WARTUNG.fr.md#2-modifier-les-textes-avec-le-classeur-excel).

### Comment les classeurs sont créés

`.github/workflows/textmappen.yml` crée après chaque modification sur `main` trois
classeurs (`scripts/texte-ausgeben.py`) et les joint à la release GitHub **« Textmappen »** –
volontairement pas sur le site. Ils ne contiennent ni brouillons ni pages protégées.

Structure : feuille de mode d'emploi (dans la langue du classeur), feuille de sommaire
(lien vers chaque page, compteur de modifications, descriptions manquantes, colonnes
Responsable/État/Remarque), puis une feuille par page dans l'ordre de la navigation.
Chaque feuille de page est un **tableau Excel** avec la colonne calculée
« Modification » – si l'on insère une ligne dans Excel, « + nouveau » y apparaît
automatiquement. (LibreOffice, Numbers et Google Sheets ne le calculent pas ; le texte
devient quand même vert.) Des colonnes masquées retiennent à quel paragraphe appartient
une ligne.

### Feuilles « Vue » pour l'accueil et l'équipe

Les feuilles « … – Vue » (onglet orange) sont construites comme le site : en-tête, étapes
de la frise et tuiles côte à côte, pour l'équipe une rangée de cartes par ressort. Seules
les cases blanches sont modifiables (protection de feuille sans mot de passe).

- Équipe : carte vide = nouvelle personne, `!Supprimer!` dans le nom = personne retirée,
  dans le titre du ressort = ressort entier retiré ; deux ressorts vides attendent en bas.
- En FR/IT, le texte allemand figure en commentaire sur la cellule.
- L'équipe de chaque langue se gère dans le classeur de cette langue.

Code : `scripts/texte_ansicht.py`.

### Feuille Uniguide

« Uniguide – Vue » montre tout le tableau de `data/unis.yaml` : une ligne par université,
une colonne par information. Les colonnes existantes, leurs noms et l'endroit où elles
apparaissent sont définis dans `data/uniguide-spalten.yaml` – et se modifient directement
dans la feuille :

- **Renommer une colonne :** écraser le nom à la ligne 4 (vaut pour la langue du
  classeur ; la petite ligne d'aide en dessous peut rester ou disparaître).
- **Supprimer une colonne :** `!Supprimer!` à la ligne 4 – la colonne disparaît avec toutes
  ses valeurs. Les colonnes dont le site a besoin (nom, langue, EMS, filières, bachelor/master
  à, site web, état, source) peuvent seulement être renommées ; le commentaire de l'en-tête
  le signale.
- **Affichage (ligne 5) :** *Tableau* = colonne dans le grand tableau, *Page* = seulement sur
  la page de l'université et dans la comparaison, *masqué* = nulle part (reste dans le
  classeur).
- **Nouvelle colonne :** à droite, trois colonnes grises vides. Inscrire le nom à la ligne 4
  et les valeurs en dessous – cela crée une nouvelle information (texte par langue, sur la
  page de l'université sous « Études & site »). Des valeurs sans nom de colonne ne sont pas
  reprises.
- **En-têtes verts** : textes par langue, valables seulement pour la langue du classeur.
  S'il manque une traduction, le site montre le texte allemand. **En-têtes foncés** :
  valables pour toutes les langues.
- Les valeurs sont du texte libre – aussi pour les places (« non limitées (env. 450
  étudiant·e·s) » est possible). Plusieurs particularités : une par ligne. Listes
  (filières, bachelor à, master à) séparées par des virgules. Langues dans n'importe quelle
  graphie (« allemand, français »). EMS : ja / nein / teilweise (oui/non/partiel). Liens
  avec `https://`.
- Une case vide ne supprime rien, `!Supprimer!` vide le champ. Les saisies invalides ne
  sont pas reprises et sont signalées dans le rapport.
- À la lecture, seul ce champ change dans `data/unis.yaml` ; les commentaires restent.
- N'inscrire que ce qui figure sur une page officielle, et modifier alors aussi « État »
  et « Source ». Une nouvelle université ne s'ajoute pas via le classeur (voir [9](#9-faq-uniguide-sous-tests-noms-de-téléchargement)).

Code : `scripts/texte_uniguide.py`.

### Feuille Questions fréquentes

« Questions fréquentes – Vue » montre toutes les questions de `data/faq.yaml` : une ligne par question avec
catégorie, question, réponse, cible du lien et texte du lien.

- **Nouvelle question :** en bas, cinq lignes vides. Inscrire question et réponse, choisir
  la catégorie dans la liste (ou en écrire une nouvelle). La question apparaît à la fin de sa
  catégorie. Dans les autres langues, le texte allemand s'affiche jusqu'à la traduction –
  dans le classeur FR/IT, la ligne est alors vide et peut être remplie.
- **Supprimer une question :** `!Supprimer!` dans la case « Question » – elle disparaît dans
  toutes les langues.
- **Cible du lien :** chemin d'une de nos pages, p. ex. `/ems/uniguide`, ou une adresse complète avec `https://` (p. ex. Discord). Si notre page n'existe
  pas, le lien n'est pas repris et c'est signalé.
- Les réponses sont du texte brut sans mise en forme (elles vont aussi dans le bloc de
  données pour les moteurs de recherche).

Code : `scripts/texte_faq.py`.

### Ce qui se passe à la lecture

`.github/workflows/texte-einlesen.yml` lit les classeurs téléversés avec
`scripts/texte-einlesen.py`, construit le site à l'essai et ouvre une pull request avec un
rapport. Chaque page modifiée est recomposée à partir des lignes de sa feuille ; les
paragraphes inchangés restent identiques au caractère près, les pages inchangées ne sont
pas touchées. Mieux vaut un message qu'un texte faux :

| Cas | Ce qui se passe |
| --- | --- |
| La page a été modifiée ailleurs entre-temps | page ignorée, le reste arrive – reporter la modification dans un classeur récent |
| Même classeur téléversé deux fois | sans dommage (« déjà repris ») |
| Cellule vide / ligne supprimée | le paragraphe reste – seul `!Supprimer!` supprime (aussi `!Löschen!`, `!Eliminare!`) |
| Tableaux, blocs, code (gris, italique) | restent inchangés ; on les modifie dans le fichier |
| Feuille triée | la page reste, message |
| Cellules déplacées au lieu de lignes entières | détecté grâce à la formule de « Modification » ; la page est reprise telle qu'elle **apparaît**, chaque paragraphe disparu figure dans le rapport |
| Ligne copiée d'une autre page, ligne grise de page supprimée | détecté et signalé |
| Titre et tous les textes avec `!Supprimer!` | la page est supprimée |
| Supprimer une page encore liée | supprimée, le rapport indique les liens (sinon la construction devient rouge) |
| Supprimer une page d'aperçu (`_index.md`) | seulement si toutes les pages en dessous sont aussi marquées |
| Page française/italienne manquante | remplir la feuille → la page est créée avec l'en-tête de la page allemande |
| Champ « nouvelle saison » de la feuille équipe | changement de saison comme en [7](#7-équipe-et-nouvelle-saison) |

« État », « Remarque » et « Responsable » ne vont pas sur le site ; le workflow les
enregistre dans `redaktion/stand.json` (seulement une somme de contrôle par texte), le
prochain classeur les reprend.

### À régler une fois

*Settings → Actions → General → Workflow permissions → « Allow GitHub Actions to create
and approve pull requests »*. Sinon la dernière étape échoue ; le rapport figure alors
dans le résumé de l'exécution. Une pull request ouverte par un workflow ne reçoit pas de
coche de `hugo.yml` (GitHub ne laisse pas un workflow en lancer un autre) – c'est pourquoi
`texte-einlesen.yml` construit lui-même et écrit ✅/❌ dans la pull request.

### Sur son propre ordinateur

```bash
pip install openpyxl pyyaml
python3 scripts/texte-ausgeben.py --uebernehmen redaktion/stand.json   # trois classeurs
python3 scripts/texte-einlesen.py ncwiki-texte-fr.xlsx --probe         # seulement afficher
python3 scripts/texte-einlesen.py ncwiki-texte-fr.xlsx                 # écrire
```

`--sprachen fr` ne crée qu'un classeur. Les classeurs n'ont pas leur place dans le dépôt
(`.gitignore`).

### Qui modifie les scripts

Le découpage d'une page en paragraphes est défini une seule fois, dans
`scripts/texte_bausteine.py`. Ensuite toujours **`python3 scripts/texte-mappe-pruefen.py`** :
il travaille dans une copie du projet comme une rédactrice (modifier, insérer, déplacer,
supprimer, feuilles « Vue », nouvelle saison, conflits …), vérifie chaque page et construit
la copie. Il ne touche pas aux vrais fichiers. Il vérifie aussi les formules des classeurs
en Python (références, plages, pas de fonctions plus récentes qu'Excel 2007). La colonne
« Texte » est au format texte, sinon Excel prendrait « - point » pour une formule.

---

## 4. Éditeur web (Pages CMS) en détail

Utilisation : [guide rapide 3](WARTUNG.fr.md#3-petites-corrections-dans-léditeur-web).

### Installation (une fois)

1. Se connecter sur [app.pagescms.org](https://app.pagescms.org) avec GitHub.
2. *Install GitHub App* et autoriser le dépôt `Kroeppster/nc-wiki`.
3. Ouvrir le dépôt, branche `main`. Les réglages sont dans [`.pages.yml`](../.pages.yml).
4. Inviter les rédacteurs·rices par e-mail sous *Collaborators* – pas besoin de compte
   GitHub.

### Ce qui s'y trouve – et ce qui n'y est volontairement pas

Par langue : **pages** (toute l'arborescence), **actualités**, **témoignages**. Créer est
possible, renommer et supprimer non (cela casse des liens).

Pas dans l'éditeur : **espace membres** et **Alpha** (un commentaire explicatif dans
l'en-tête serait perdu), **`data/*.yaml`** (plein de commentaires que l'éditeur
effacerait), **téléverser des images**.

### Ce que l'éditeur change aux fichiers

À l'enregistrement, Pages CMS réécrit tout le fichier : les guillemets de l'en-tête
disparaissent, les longs textes sont coupés, les listes écrites l'une sous l'autre, `&`
devient `&amp;`, les tableaux sont réalignés. Pour Hugo, c'est la même chose.
`scripts/editor-rundlauf.mjs` enregistre chaque page comme le fait Pages CMS, construit les
deux versions et compare – dernièrement 440 pages sur 440 identiques. Les classeurs Excel
s'en accommodent.

### Qui modifie `.pages.yml`

- **`settings.content.merge: true` doit rester.** Sinon Pages CMS ne réécrit que les
  champs qui y sont nommés – menu, ordre, tags et l'accueil (`hero`, `weg`, `material`)
  disparaîtraient au premier enregistrement.
- Ensuite `node scripts/editor-rundlauf.mjs` (nécessite une fois quelques paquets npm
  dans un dossier à part, voir l'en-tête du script).
- Pages CMS refuse les clés inconnues ; les champs réutilisés sont donc des ancres YAML
  (`&titel`, `*titel`) dans la partie allemande.

---

## 5. Liens, blocs et contenus programmés

### Liens internes

Liens Markdown normaux avec le chemin, sans langue ni `/nc-wiki/` :
`[Uniguide](/ems/uniguide)`. Le hook `layouts/_default/_markup/render-link.html` en fait
l'adresse correcte dans la langue de la page et arrête la construction si la cible
n'existe pas.

**Pas de `{{< ref >}}` ni d'autres shortcodes dans le texte.** L'éditeur web les casse à
l'enregistrement – même si quelqu'un ne change qu'une virgule sur la page.

### Blocs

Bloc de code avec la langue `baustein` (`layouts/_default/_markup/render-codeblock-baustein.html`) :

| Nom | Quoi | Données |
| --- | --- | --- |
| `testablauf` | tableau du déroulement | `data/testablauf.yaml` |
| `team-leitung` | cartes de l'équipe dirigeante | `ressorts:` dans l'en-tête de la page équipe |
| `fakten-generator` | générateur de faits | `data/fakten-generator/` |
| `figuren-generator` | générateur de figures | – |
| `sponsoring-kontakt` | bouton e-mail/téléphone | `data/sponsoring.yaml` |
| `antwortbogen-auswertung` | évaluer la feuille de réponses par photo (Alpha) | `data/antwortbogen.yaml` |
| `konztest-auswertung` | évaluer le test de concentration par photo (Alpha) | `data/konztest.yaml` |

Une faute de frappe dans le nom arrête la construction. Nouveaux blocs : créer un partial
sous `layouts/partials/bausteine/` et ajouter le nom à la liste `$erlaubt` du hook.

### Afficher quelque chose à partir d'une heure donnée

```
{{< reveal-at when="2027-02-10T22:00:00+01:00" >}}
[S'inscrire maintenant](https://...)
{{< /reveal-at >}}
```

Le fuseau horaire est obligatoire (`+01:00` hiver, `+02:00` été) ; sans date valable, le
contenu reste caché. Le masquage se fait seulement dans le navigateur – pas pour du
secret. **Attention :** c'est un shortcode. Ne plus enregistrer la page dans l'éditeur
web ensuite, et retirer le bloc après l'échéance.

---

## 6. Page d'accueil

L'accueil est construit à partir de l'**en-tête** de `content/de|fr|it/_index.md` (modèle
`layouts/index.html`). Les textes se modifient le plus facilement avec la feuille
« … – Vue » de l'accueil dans le classeur ; sinon dans les trois fichiers.

### Ordre des sections

Hero → actualités → « Ce dont tu as besoin, et quand » (frise) → « Le matériel » → les
huit sous-tests → mission → bande de marque → appel aux dons. Réordonner : déplacer les
blocs `<section>` dans `layouts/index.html` et répartir la classe `section-surface` de
sorte que sections claires et teintées alternent.

### Hero

```yaml
hero:
  bild: "testsimulationen/testsimulation-2023.jpg"   # relatif à assets/images/
  bild_alt: "Amphithéâtre plein pendant une simulation …"
```

`bild_alt` est obligatoire dès qu'une image est définie (traduit dans chaque langue). Sans
`bild`, pas de photo. La photo doit montrer que tout ceci est réel – pas d'image
symbolique.

### Frise (`weg:`)

```yaml
weg:
  start: "2026-10-01"            # début de l'axe
  ende: "2027-09-30"             # fin de l'axe
  termine:
    - wann: "Dez. bis 15. Feb."  # texte tel qu'affiché
      titel: "Voranmeldung bei swissuniversities"
      von: "2026-12-01"          # détermine la position sur l'axe
      bis: "2027-02-15"          # sans = un seul jour
      art: "offiziell"           # offiziell | angebot
      fuer: "mit"                # mit | ohne | beide (sélecteur avec/sans EMS)
    - wann: "Februar bis Mai"
      titel: "Technik aufbauen"
      text: "…"                  # affiché seulement pour l'offre
      von: "2027-02-16"
      bis: "2027-04-30"
      art: "angebot"
      fuer: "beide"
      mittel:                    # liens, seulement pour l'offre
        - titel: "Uniguide"
          url: "ems/uniguide/"
```

Un axe du temps continu d'octobre à septembre : **chaque entrée se place automatiquement là où
se trouve sa date** (`von`/`bis`). En haut les dates officielles de swissuniversities, en
dessous notre offre ; les textes qui se chevaucheraient passent d'eux-mêmes sur une autre
ligne. Un sélecteur bascule entre les dates pour les universités avec et sans EMS (`fuer`).
Nouvelle saison : modifier `start`, `ende` et les années des dates, dans les trois langues.
Tout se trouve dans le classeur, feuille « Accueil – Vue », sous forme de tableau (une ligne
par entrée ; **nouvelles entrées** : remplir une des lignes vides en bas, titre et début requis ;
suppression avec `!Supprimer!` dans le titre ; liens « Titre | ems/uniguide/ », une ligne par
lien). Code : `scripts/texte_zeitstrahl.py`. Ne modifier les dates que si elles figurent ainsi chez swissuniversities.
Sur mobile, cela devient une liste verticale par date. Calcul :
`layouts/partials/weg-positionen.html`, affichage `weg-grid.html`.

### Tuiles du matériel (`material:`)

```yaml
material:
  items:
    - key: uebungsaufgaben        # ne pas traduire
      titel: "Séries d'exercices"
      zahlen: ["uebungen"]        # remplit {1}
      text: "{1} séries pour les huit sous-tests, avec solutions."
```

`key` autorisés : `uebungsaufgaben`, `testsimulationen`, `vorbereitungskurse`, `community`.

**Ne jamais écrire les nombres à la main.** `layouts/partials/angebot-zahlen.html` recompte
à chaque construction : séries sans les PDF de solution, simulations par millésime,
universités et questions depuis les fichiers de données, témoignages par langue. Dans le
texte on met `{1}`, `{2}` …

Les images d'une tuile sont définies dans `layouts/partials/material-grid.html` (bloc
`$quellen`). Les pages de PDF sont toujours montrées **entières** (`papier: true`, fond
blanc, `object-fit: contain`) – les PDF sources sont en partie A4, en partie US Letter. Les
photos peuvent être recadrées. Un nom avec extension est cherché sous `assets/images/`,
sans extension sous `assets/images/angebot/`. Regénérer avec
`python3 scripts/angebot-bilder-erzeugen.py` (nécessite `pip install pymupdf` ; en haut du
script figurent le PDF et la page de chaque image). La carte Discord n'est volontairement
pas une fausse capture d'écran.

Retirer ou réordonner étapes et tuiles : supprimer ou déplacer l'entrée dans les trois
fichiers. Une tuile entièrement nouvelle nécessite une entrée dans `$quellen` (étape de
développement).

Attention dans le modèle : un commentaire Hugo `{{/* */}}` à l'intérieur d'un `dict` casse
la construction.

---

## 7. Équipe et nouvelle saison

### Équipe dirigeante

Elle figure dans l'en-tête de `content/<langue>/ueber-uns/team/_index.md` sous
`ressorts:` ; le bloc `team-leitung` en fait les cartes.

```yaml
ressorts:
  - titel: "Présidence"
    mitglieder:
      - name: "Prénom Nom"
        rolle: "Co-président"
        foto: "team/prenom-nom.jpg"   # facultatif, relatif à assets/images/
```

L'ordre des blocs = l'ordre sur la page. Sans photo, un cercle coloré avec les initiales
apparaît. Les noms sont identiques dans toutes les langues, `titel` et `rolle` sont
traduits. Le plus simple : la feuille « … – Vue » de l'équipe dans le classeur.

### Nouvelle saison

Deux voies qui font la même chose (`scripts/texte_saison.py`) :

- dans le classeur, feuille « … – Vue » de l'équipe, remplir « Commencer une nouvelle
  saison » et téléverser, **ou**
- sur GitHub *Actions → Neue Saison starten → Run workflow*, inscrire la saison (donne une
  pull request).

Dans les trois langues, la section « Équipe saison … » passe avec une liste de l'équipe
dirigeante dans les archives (`ueber-uns/archiv/`, tout en haut sous les saisons
précédentes), et la page équipe commence la nouvelle saison avec une phrase provisoire.
L'équipe dirigeante elle-même reste ; les changements se font ensuite. Une seconde
exécution avec la même saison ne fait rien.

### Archives

`content/<langue>/ueber-uns/archiv/_index.md` est du texte normal : saisons précédentes,
anciens responsables, anciens scripts de cours (liste automatique depuis
`assets/downloads/archiv-kursskripte/`) et en dessous les anciennes actualités
(`ueber-uns/archiv/news/`).

---

## 8. Soutien, dons, sponsors

### « Soutenir maintenant »

`content/<langue>/unterstuetzer-innen/jetzt-unterstuetzen.md` a `layout: spenden`
(`layouts/_default/spenden.html`) :

- le **premier** intertitre `##` avec son texte figure à gauche du grand code TWINT, en
  dessous le bouton « Faire un don par virement » ;
- le **deuxième** intertitre `##` forme la partie sponsoring avec le bouton « Plus
  d'informations » (vers la page Sponsors).

Les textes restent donc du texte normal (classeur, éditeur). Libellés des boutons : `i18n`,
préfixe `spenden_`. Changer le code TWINT : remplacer
`assets/images/unterstuetzen/twint-qr.png` (carré). Il reste sur fond blanc même en mode
sombre, pour que l'app le lise. Les coordonnées bancaires sont sur
`unterstuetzer-innen/spenden-ueberweisung.md`. Pas encore de paiement par carte.

### Page Sponsors

`unterstuetzer-innen/sponsoren.md` est du texte normal ; à la fin figure le bloc
`sponsoring-kontakt`. E-mail et téléphone dans `data/sponsoring.yaml` – si `telefon` est
vide, aucun bouton téléphone n'apparaît.

### Logos des sponsors

Les logos de « Nos soutiens » viennent de `data/sponsors.yaml` (expliqué champ par champ
dans le fichier) :

1. Téléverser le logo dans `assets/images/sponsors/` (SVG de préférence).
2. Ajouter une entrée :

   ```yaml
   - name: "Nom de l'entreprise"
     logo: "fichier.svg"
     website: "https://exemple.ch/"
   ```

L'ordre dans le fichier = l'ordre des tuiles. Retirer : supprimer l'entrée. Les logos
sombres reçoivent automatiquement un fond clair (`.sponsor-logo`).

---

## 9. FAQ, Uniguide, sous-tests, noms de téléchargement

### FAQ (`data/faq.yaml`)

Le plus simple : la feuille « Questions fréquentes – Vue » du classeur ([3](#3-classeurs-excel-en-détail)). Dans le fichier :

```yaml
- id: "identifiant-unique"
  category: { de: "…", fr: "…", it: "…" }
  question:
    de: "…?"
  answer:
    de: "…"
  link:
    href: "ems/uniguide/"
    label:
      de: "…"
```

La page regroupe par catégorie, dans l'ordre du fichier. La question « Quels sont les
sous-tests ? » ajoute automatiquement la liste de `data/subtests.yaml`
(`dynamic: subtests`) ; la phrase qui précède (« 9 sous-tests ») est fixe dans la FAQ.

### Uniguide (`data/unis.yaml`, `data/uniguide-spalten.yaml`)

Les valeurs sont dans `data/unis.yaml` ; les informations existantes, leurs noms, si elles
apparaissent comme colonne du tableau, seulement sur la page de l'université ou nulle part,
et dans quelle section de la page, sont dans `data/uniguide-spalten.yaml` (description des
champs en tête du fichier). Tableau, comparaison et page de l'université s'en construisent
tout seuls – une nouvelle colonne ne demande pas de code. Chaque université a besoin en plus
d'une page presque vide `content/<langue>/ems/uniguide/<slug>.md` avec `title` et
`uni_slug`. Le plus simple : la feuille « Uniguide – Vue » du classeur ([3](#3-classeurs-excel-en-détail)).

Une valeur simple (`semestergebuehr: "CHF 850"`) vaut pour toutes les langues, sinon par
langue (`de:`/`fr:`/`it:`). Les noms des langues d'enseignement viennent de `i18n`
(`sprache_…`). « Lieu d'études » est la ville ; l'avantage du domicile a sa propre colonne ;
« Bachelor à » et « Master à » indiquent où se font les deux niveaux.

**Ne rien estimer.** Un champ reste `null` jusqu'à ce que la valeur figure sur une page
officielle – alors modifier aussi `stand` (date) et `quelle` (lien). Les places proviennent
des capacités d'accueil de swissuniversities (mention de source dans le champ `hinweis` de
la colonne). Les champs vides n'apparaissent pas ; les colonnes avec `fehlt: true` figurent
alors dans le cadre « Ces informations manquent encore » de la page de l'université.

`berichte_ort` doit correspondre exactement à l'`ort:` des témoignages ; les trois plus
récents apparaissent alors sur la page de l'université. La comparaison permet jusqu'à quatre
universités côte à côte (`var MAX = 4` dans `layouts/partials/uniguide-table.html`).

### Sous-tests (`data/subtests.yaml`)

Alimente les tuiles des sous-tests. **L'ordre = l'ordre le jour du test** et doit
correspondre à `data/testablauf.yaml`. `slug` = nom du dossier sous
`content/<langue>/ems/uebungsaufgaben/` ; `number` n'est pas affiché. En réordonnant,
adapter aussi le `weight` des pages d'exercices. Le site a 8 pages d'exercices, car
« Figures & faits » regroupe deux sous-tests officiels – le vrai EMS en a 9.

Une remarque supplémentaire près des téléchargements d'une page d'exercices :
`downloads_notice: "Nouvelle mise en page !"` dans l'en-tête (par langue).

### Noms de téléchargement (`data/downloads.yaml`)

Les séries d'exercices et les simulations de test apparaissent regroupées par année (la plus
récente est dépliée). Pour les séries, l'intitulé (« Série 2 », boutons « Exercices » et
« Corrigé ») est créé automatiquement à partir du nom de fichier. Si le corrigé se trouve
dans le même PDF, le nom du fichier va sous `mit_loesung:` – le bouton s'appelle alors
« Exercices avec corrigé ». Tous les autres fichiers (cahiers de test, évaluations, scripts
de cours) reçoivent sous `overrides:` un nom avec traductions, sans l'année pour les
simulations de test. Le format est expliqué en tête du fichier.

---

## 10. Mode examen

`/ems/pruefungsmodus/` : lit les consignes à voix haute, affiche une horloge plein écran et
dit « Stop » – pour un sous-test ou toute la journée sans pauses. Les exercices viennent
des PDF.

### Durées et ordre

Tout dans **`data/testablauf.yaml`** : blocs dans l'ordre du jour du test avec `minuten`,
nombre d'exercices, points et noms dans les trois langues. Le fichier alimente le tableau
sur `/ems/` (bloc `testablauf`), le mode examen et les durées par défaut des générateurs.
Le temps total est additionné. **Modifier avec soin** – un chiffre faux signifie des mois
d'entraînement avec une mauvaise durée.

### Déroulement personnalisé

- **Normal :** choisir sous-tests et nombre d'exercices ; le temps se calcule au rythme du
  vrai EMS (7 exercices « Muster zuordnen » = 6:13). En interne, on calcule en
  **secondes**.
- `aufgaben_fest: true` (mémoriser figures/faits) : c'est le **temps** qui est réglable au
  lieu du nombre.
- **Mode expert :** minutes et pauses libres. Un lien partagé qui en a besoin l'active
  lui-même. Format du temps dans le lien `6m13` (un nombre seul vaut des minutes, les
  anciens liens restent valables).
- La composition se partage par lien ; rien n'est enregistré sur un serveur.

### Annonces

Textes dans `i18n/*.yaml`, préfixe `pm_` – courts, sans parenthèses ni abréviations, car
ils sont prononcés. Vouvoiement, comme un·e surveillant·e. Pour DE et FR, 15
enregistrements se trouvent sous `assets/audio/pruefungsmodus/<langue>/` (liste dans le
README ; voix française sous CC-BY 4.0, attribution dans le README) ; un enregistrement a
priorité sur la synthèse vocale du navigateur. En italien, l'appareil lit. Après une
modification d'un texte `pm_`, supprimer l'enregistrement ou le regénérer avec
`scripts/ansagen-erzeugen.py`. Vrais enregistrements de l'association : écraser le fichier
de même nom.

### Technique à connaître

- L'horloge retient une **heure de fin** au lieu de compter les secondes (les navigateurs
  ralentissent les onglets en arrière-plan).
- Wake-Lock garde l'écran allumé ; le plein écran n'est qu'un bonus.
- Pas d'attente entre les blocs, aucune heure de fin affichée, la pause est marquée
  « seulement pour s'entraîner ».
- Nombre d'exercices/temps modifié → la phrase est lue au lieu de l'enregistrement (qui
  cite les vraies valeurs). `{dauer}` utilise `pm_dauer_min`/`pm_dauer_min_sek`.
- Ne pas retirer `safeJS` dans `layouts/partials/pruefungsmodus.html` – sinon la page reste
  muette.

---

## 11. Générateurs d'apprentissage et page Alpha

Le matériel pour « Figures & faits » ne sert qu'une fois – deux générateurs tirent donc
toujours de nouveaux sets. Les deux se jouent à l'écran avec horloge ou s'impriment comme
cahier de six pages (consigne, page de mémorisation, questions, feuille de réponses,
corrigé ; en-tête, numéro de page, logo CC-BY-NC). Durées et pause (le vrai intervalle le
jour du test) viennent de `data/testablauf.yaml`.

**État actuel :** les deux générateurs se trouvent pour l'instant seulement sur la
[page Alpha](#page-alpha) (`content/de/alpha/_index.md`), pas sur la page publique
« Figures & faits ». Pour les valider, remettre le bloc dans le texte de la page d'exercices
(dans les trois langues, avec la mention du générateur dans « Pièges typiques »).

### Format du cahier

Mesures tirées de l'**outil de formatage NCWiki** privé (`vorlage/ems.typ`). Cadre commun :
`layouts/partials/bausteine/ems-heft.html`, styles dans `assets/css/style.css`
(« EMS-Heft »). Modifier une mesure d'abord dans l'outil, puis reprendre le même chiffre.
**Ne reprendre que le format, jamais le contenu** – l'outil est privé, le site public.
Avant de toucher aux règles d'impression, lire le commentaire à `@media print` (les pages
du cahier vont dans un conteneur à part sous `<body>` ; règles attachées à
`body.fg-druckt`).
État : `ems.typ` après l'alignement sur les fichiers InDesign du Probelauf 2026 (marges
15 mm, première ligne de base 98.66, cadre, flèche et STOP, grille des figures, questions
de faits sur deux colonnes à places fixes, grille de correction). Les consignes suivent le
texte du cahier officiel dans `i18n` (`fg_anl_*`, `fig_anl_*`, `ems_*`). Pour vérifier :
imprimer un set (« Enregistrer en PDF ») et comparer la position des textes et des lignes
avec la feuille de l'outil (p. ex. avec `pymupdf`) ; écarts tolérés sous 1 pt (le
navigateur arrondit aux pixels).

### Générateur de faits

Listes de mots dans `data/fakten-generator/<langue>.yaml` (actuellement seulement
`de.yaml` ; dès qu'un `fr.yaml`/`it.yaml` existe, il apparaît tout seul). Ne pas dissoudre
les catégories : une vraie série donne à chaque groupe d'âge trois professions d'**un**
domaine et trois maladies de **trois** sortes. Les questions naissent de modèles de phrases
(`fragen`), plus `namensgruppen`, `dativ`, `nicht_attributiv`.
`scripts/fakten-listen-auslesen.py` extrait des mots des PDF mais n'écrase pas le YAML. En
suspens : catégories pas encore validées par un humain ; ~40 au lieu de ~80 entrées par
catégorie.

**Gestion par Excel** (fichier propre, pas les classeurs de textes) : `ncwiki-wortliste-fakten-generator.xlsx`,
toujours à jour sous *Releases → Textmappen* (https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-wortliste-fakten-generator.xlsx).
Une feuille par liste (Namensgruppen, Einzelne Namen, Berufe, Krankheiten, Merkmale, Dativ-Plural), plus
« Anleitung » et « Übersicht » (compte par formules si les quantités minimales sont atteintes). Modifier,
enregistrer, téléverser dans `redaktion/` (le nom commence par `ncwiki-wortliste`) : `wortliste-einlesen.yml`
vérifie le fichier avec `scripts/wortliste.py` et ouvre une pull request avec rapport (nouveau / supprimé /
remarques). **En cas d'erreur**, rien n'est repris et aucune pull request n'est ouverte ; l'exécution devient
rouge et son résumé nomme chaque erreur avec feuille et ligne (trop peu de mots, mot en double, sexe autre que
m/w, caractères `< > & { }`). Quantités minimales : 15 noms isolés ; au moins 5 champs professionnels avec au
moins 3 professions chacun ; au moins 3 types de maladies et 15 maladies ; au moins 15 caractéristiques en
minuscules. L'Excel remplace la liste **entière** (instantané) ; si elle repose sur un état plus ancien, le
rapport avertit. Seuls les blocs de mots sont remplacés – le commentaire explicatif, les groupes d'âge et les
modèles de questions restent. Un nouveau champ ou type naît en saisissant un nouveau nom (court, minuscules,
sans espace ; « Technik und Bau » donnerait un NOUVEAU champ `technik_und_bau`, donc utiliser la liste de
choix). En local : `python3 scripts/wortliste.py ausgeben` ou `einlesen FICHIER [--probe]` ; après des
modifications du script `python3 scripts/wortliste-pruefen.py`.

### Générateur de figures

Pas de fichier de données, libellés dans `i18n` (préfixe `fig_`). Chaque **série** tire
d'abord son style (angles, dentelure, taille, construction libre/moyeu/bandes), les 18
figures le suivent – sinon toutes les séries se ressembleraient. Mesurer plutôt
qu'estimer : `python3 scripts/figuren-vergleichen.py 14 [--original <PDF>]` (nécessite
`pymupdf numpy scipy pillow` ; le PDF d'exemple officiel de swissuniversities n'est pas
dans le dépôt). Avant de toucher au dessin, lire l'en-tête de commentaires de
`layouts/partials/bausteine/figuren-generator.html` – les erreurs passées y figurent
(identifiants de clip en double, champs qui se fragmentent, contours lissés séparément,
lettres au centre de gravité, logo mesuré comme figure).

### Page Alpha

`content/de/alpha/` est l'établi des nouvelles fonctions : protégée par mot de passe, liée
nulle part, **seulement en allemand**. Une section par fonction, qui dit ce qu'il faut
évaluer. Une fois validée, le bloc passe sur la vraie page (alors en trois langues).
Actuellement : générateur de figures, générateur de faits, « Antwortbogen auswerten » et « Konzentrationstest auswerten ».

### Évaluer la feuille de réponses (Alpha)

Une photo de la feuille de réponses remplie d'une simulation est lue dans le navigateur et
comparée aux solutions – la photo ne quitte pas l'appareil. Le procédé est celui de l'outil
de formatage (`werkzeug/auswertung.py`), transposé en JavaScript
(`layouts/partials/bausteine/antwortbogen-auswertung.html`, lire le commentaire d'en-tête ;
le commun – image, chargement, PDF, caméra en direct – est dans `bausteine/bild-lesen.html`).
La **caméra en direct** cherche les quatre coins noirs dès le viseur et déclenche seule dès que
la feuille ne bouge plus ; sinon reste « Prendre une photo » (appli caméra).
Toutes les simulations depuis 2022 ont la même feuille. Les solutions sont dans
`data/antwortbogen.yaml` et ne se modifient **pas à la main** : pour une nouvelle
simulation, téléverser le PDF des solutions comme d'habitude, l'inscrire dans
`scripts/antwortbogen-loesungen.py` et lancer `python3 scripts/antwortbogen-loesungen.py
--schreiben` (s'arrête s'il ne trouve pas exactement 144 solutions). Pour les simulations qui
ne sont pas sur le site, il y a « Eigener Lösungsschlüssel » : le PDF des solutions de l'outil
(ou une photo de la page de la grille de correction) est lu comme une feuille remplie, les
cases noires sont les solutions ; les lignes sans case ne comptent pas. Les PDF sont ouverts
par pdf.js depuis `static/vendor/pdfjs/` (volontairement pas depuis un CDN : rien ne doit
quitter l'appareil ; pour mettre à jour, remplacer les deux `.mjs` du paquet npm
`pdfjs-dist`). Après une modification
de la lecture : `python3 scripts/antwortbogen-testbilder.py /tmp/ab` (photos de test aux
croix connues) puis `node scripts/antwortbogen-pruefen.mjs /tmp/ab`.

### Évaluer le test de concentration (Alpha)

Comme la feuille de réponses, mais selon le procédé de `werkzeug/konztest_auswertung.py` : la
feuille n'a pas de marques de repérage, la grille des 1600 signes sert elle-même de repère
(taches magenta → grille → position par la ressemblance des signes identiques → transformation
→ encre par signe). Comptage selon la consigne : justes moins faux moins signes cibles omis
avant le dernier signe marqué (valeur brute) ; une barre violette montre ce dernier. Toucher l'image inverse une marque.
Encre par signe : de combien c'est plus sombre que le papier juste à côté (les ombres ne gênent donc
pas), moins ce que le même signe sans marque a au même endroit. Le seuil « marqué » se déduit de chaque
image ; si les traits ne ressortent pas nettement (trop de cas douteux, reflet), la page demande une
nouvelle photo au lieu d'un résultat incertain. Partial
`layouts/partials/bausteine/konztest-auswertung.html`. Grille, position et solution de tous les
tests de concentration du site avec feuille de solutions dans `data/konztest.yaml`, généré par
`python3 scripts/konztest-loesungen.py --schreiben` : dessiner la page du test, trouver les
40 × 40 signes comme taches, regrouper les signes identiques en classes ; dans la feuille de
solutions, chercher les cases remplies et les poser sur la grille. Contrôles : 40 × 40 trouvés,
solution univoque, « 10 par ligne » là où c'est prescrit, et l'épreuve de la règle (chaque
règle ne dépend que du signe et d'un voisin). Un nouveau test va dans la liste `KONZTESTS` du
script. Absents : simulations 2024 et 2025 et séries 2025 S18/S19 (pas de feuille de solutions
sur le site), 2021 S03 (cases posées à la main, pas univoques), 2022 S02 (signes imprimés en
noir – un test de concentration a toujours les signes en couleur ; la page refuse les tests
chargés imprimés en noir). **Propre test :** dans la
liste, « Propre test de concentration », charger l'énoncé et la feuille de solutions en PDF (un
ou deux fichiers) ; le bloc `konztest-lesen.html` les lit avec le même procédé dans le
navigateur et les garde en mémoire. Si le procédé change, adapter les deux –
`scripts/konztest-pruefen.mjs` compare navigateur et script sur des PDF du site. Vérifier :
`python3 scripts/konztest-testbilder.py /tmp/kt` puis `node scripts/konztest-pruefen.mjs /tmp/kt`
(depuis le dossier du dépôt).

---

## 12. Espace membres

`content/<langue>/mitglieder/` – pas dans le menu, chiffré par mot de passe à la
publication (StatiCrypt, `scripts/encrypt-protected-pages.mjs`).

### Ce que la protection apporte

Elle tient à l'écart moteurs de recherche et visites fortuites, mais **n'est pas un
login** : un mot de passe commun ; la page chiffrée est publique et peut être attaquée
hors ligne ; **les PDF liés ne sont pas protégés** (qui connaît l'adresse peut les
télécharger). Donc seulement de l'interne sans risque – pas de données personnelles,
relevés bancaires, candidatures.

### Nouvelle page protégée

Comme toute page, plus `geschuetzt: true` dans l'en-tête (dans les trois langues). Cela
met `noindex`, retire la page de la recherche, du sitemap et du RSS et la chiffre. Liste de
PDF : `download_ordner: "downloads/mitglieder"`.

### Mot de passe

- Valable **deux heures** après le dernier accès, pour toutes les pages membres et langues
  (`MERKDAUER_MINUTEN` dans `scripts/passwort-vorlage.html`). Le navigateur garde une
  valeur de contrôle salée, pas le mot de passe. Se déconnecter : ajouter
  `?staticrypt_logout` à l'adresse.
- **Changer :** *Settings → Secrets and variables → Actions →* `MITGLIEDER_PASSWORT` →
  nouveau mot de passe (au moins 16 caractères aléatoires) → puis *Actions → Deploy Hugo
  site to GitHub Pages → Run workflow*. Nouveau mot de passe dans le gestionnaire et aux
  membres. Le `SALZ` du script reste.
- **Construction rouge avec « Kein Passwort gesetzt » :** le secret manque – la
  construction s'arrête volontairement au lieu de publier en clair. Pour les pull requests,
  seulement un avertissement.
- En local : `npm run build && STATICRYPT_PASSWORD='test' npm run schuetzen`, résultat dans
  `public/mitglieder/`.

---

## 13. Formulaires

Le site n'a pas de serveur ; les formulaires passent par **Formspree**.

| Formulaire | Où | ID Formspree | Fichier |
| --- | --- | --- | --- |
| Contact | `/kontakt/` | `mvkpgrpl` | `layouts/partials/contact-form.html` |
| Signaler une erreur (exercices) | pages d'exercices | aussi `mvkpgrpl` | `layouts/partials/report-error-general.html` |
| Témoignage | `/ems/erfahrungsberichte/` | `xaewqwoj` | `layouts/partials/experience-form.html` |

Les signalements arrivent provisoirement dans la boîte de contact, avec l'objet fixe
« Fehlermeldung Uebungsaufgaben (Website) » pour filtrer. Adresse propre plus tard :
l'inscrire seulement dans `report-error-general.html`.

**Ne pas changer l'adresse des témoignages :** un envoi déclenche via
`repository_dispatch` le workflow `erfahrungsbericht-intake.yml`, qui crée fichier et pull
request (le jeton GitHub nécessaire n'est enregistré que dans Formspree).

L'envoi en arrière-plan est assuré par un script commun dans
`layouts/partials/footer.html` pour tous les formulaires de classe `report-error`. Un
nouveau formulaire à un nouvel endroit est une étape de développement.

---

## 14. Réglages dans hugo.toml

Sous `[params]` :

| Champ | Effet |
| --- | --- |
| `ems_exam_date = '2027-07-09T08:00:00+02:00'` | cible du compte à rebours de l'accueil (fuseau obligatoire) |
| `google_analytics_id` | Google Analytics ; vide = désactivé |
| `social_instagram`, `social_discord`, `social_linkedin` | boutons du pied de page ; vide = pas de bouton |
| `newsletter_url` | inscription à la newsletter ; vide = pas de bloc newsletter |

Google Analytics ne se charge **que** si « Accepter » a été choisi dans la bannière cookies.
Textes de la bannière : `i18n`, préfixe `cookie_`.

---

## 15. Textes fixes (i18n)

`i18n/de.yaml`, `fr.yaml`, `it.yaml` contiennent tous les textes qui n'appartiennent pas à
une page : boutons, formulaires, bannière cookies, annonces, libellés. À gauche la clé, à
droite le texte ; **les trois fichiers ont les mêmes clés**. Toujours modifier un texte
dans les trois fichiers. Une nouvelle clé n'agit que si elle est utilisée dans `layouts/`.

---

## 16. Design : couleurs, police, logo, liste des sections

### Couleurs

Tout dans `assets/css/style.css`, en haut sous forme de variables. Il y a **deux
palettes** : `:root{…}` (claire) et `:root[data-theme="dark"]{…}` (sombre) – toujours
modifier une couleur dans les deux.

- `--color-signal` est la couleur des liens et de la marque, `--color-btn-bg` le fond des
  boutons pleins. En mode sombre elles diffèrent volontairement (lien clair, mais assez de
  contraste pour le texte blanc des boutons) – adapter les deux.
- `--cta-from`/`--cta-to` et `--color-avatar-0…5` n'existent qu'en clair, car du texte blanc
  s'y pose – ne jamais les rendre trop clairs.
- Profondeur : `--shadow-sm|md|lg`, `--glow-*`, `--band-*`, `--color-section-alt`. Les ombres
  sont plus fortes en mode sombre.
- Avant tout changement de couleur, vérifier le contraste (« WCAG contrast checker ») :
  texte 4.5 : 1, grands titres 3 : 1, dans les deux modes.

### Police

**Poppins** (titres) et **Inter** (texte), servies depuis `static/fonts/` (pas chargées chez
Google – protection des données). Remplacer : déposer le `.woff2` là **et** adapter le bloc
`@font-face` ainsi que `--font-display`/`--font-body`.

### Logo et favicon

Logo : `static/images/logo.svg` (en-tête, hero, bande de marque). Il est dessiné en foncé et
devient blanc par filtre en mode sombre et dans la bande sombre (`--logo-filter`,
`.brand-band-logo`). Un nouveau logo multicolore a besoin d'une solution propre. Le favicon
(`static/favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`) n'est pas généré
automatiquement – avec un nouveau logo, le refaire avec un outil d'image ou de favicon et le
téléverser sous les mêmes noms.

### Liste des sections (« Sur cette page »)

Naît automatiquement des intertitres `##` (à partir de deux). Dès 1100 px à droite du texte,
en dessous repliée au-dessus du texte. Code : `layouts/partials/seiten-uebersicht.html`,
grille `.seite-raster`/`.mit-liste` dans `single.html`/`list.html`, libellé
`auf_dieser_seite`. Ne pas revenir à : bloc entre titre et texte, barre qui n'apparaît qu'au
défilement, rangée horizontale défilante. Le script attend `DOMContentLoaded`, recueille
aussi les titres venant de modèles, prend sa place dans la marge (`--rand-ausbruch`) et a
besoin de `--sprung-abstand`/`--kopf-hoehe` pour que les ancres ne finissent pas sous
l'en-tête.

---

## 17. Supprimer toute une rubrique

- Supprimer `_index.md` et toutes les pages en dessous, **dans les trois langues**. L'entrée
  de menu disparaît avec.
- La construction reste rouge tant que des liens pointent vers la rubrique – adapter ces
  endroits.
- PDF et images sous `assets/` ou `static/` ne sont pas supprimés avec.
- Alternative dans le classeur : marquer le titre et tous les textes avec `!Supprimer!`.

---

## 18. Automatisations (GitHub Actions)

| Workflow | Quand | Quoi |
| --- | --- | --- |
| `hugo.yml` | chaque modification de `main`, chaque pull request | construire, recherche (Pagefind), vérifier les liens internes (bloque), liens externes (avertissement), chiffrer l'espace membres, publier (seulement `main`) |
| `textmappen.yml` | chaque modification de `main` | classeurs récents dans la release « Textmappen » |
| `texte-einlesen.yml` | classeur téléversé dans `redaktion/` | lire, construire à l'essai, pull request avec rapport |
| `wortliste-einlesen.yml` | `ncwiki-wortliste*.xlsx` téléversé dans `redaktion/` | vérifier, lire, construire à l'essai, pull request avec rapport ; en cas d'erreur pas de pull request, exécution rouge |
| `neue-saison.yml` | à la main (*Run workflow*) | changement de saison en pull request |
| `erfahrungsbericht-intake.yml` | envoi Formspree | nouveau témoignage en pull request |

Une construction ratée ne met pas le site hors ligne ; la dernière bonne version reste.
Version de Hugo : fixée dans `hugo.yml` – en l'augmentant, tester aussi en local.

---

## 19. Vérifier le site

La construction vérifie elle-même les liens internes. Il existe en plus des scripts de
vérification (en local, avec le site construit sous `public/`) :

```bash
npm run build
npx http-server public -p 8099 -s &
BREITEN=1280,768,390 MODI=light,dark node scripts/seiten-pruefen.mjs  # mise en page, contraste, images
python3 scripts/struktur-pruefen.py                                  # doublons, pages inaccessibles, liens morts
npx pagefind --site public && node scripts/verhalten-pruefen.mjs     # utilisation, formulaires (Formspree intercepté)
node scripts/fakten-generator-pruefen.mjs                            # 150 sets + PDF
node scripts/figuren-generator-pruefen.mjs                           # 12 sets + PDF
python3 scripts/antwortbogen-testbilder.py /tmp/ab && node scripts/antwortbogen-pruefen.mjs /tmp/ab  # photos de feuilles
python3 scripts/konztest-testbilder.py /tmp/kt && node scripts/konztest-pruefen.mjs /tmp/kt              # photos du test de concentration
python3 scripts/texte-mappe-pruefen.py                               # classeurs
python3 scripts/wortliste-pruefen.py                                 # liste de mots (Excel)
node scripts/editor-rundlauf.mjs                                     # éditeur web
```

Autre port : `ADRESSE=http://127.0.0.1:8123` devant. Attendu : exactement dix pages
inaccessibles (espace membres et Alpha). Tester d'abord une nouvelle vérification sur une
vraie erreur connue et supprimer les fausses alertes – sinon plus personne ne la lit.

---

## 20. Services tiers et accès

| Service | Pour quoi |
| --- | --- |
| GitHub Pages / Actions | hébergement et automatisation. Le passage à `nc-wiki.ch` est préparé mais pas actif (pas de `CNAME`, DNS pas modifié). |
| Formspree | formulaires ([13](#13-formulaires)) |
| Pages CMS | éditeur web ([4](#4-éditeur-web-pages-cms-en-détail)) |
| Pagefind | recherche, tourne entièrement dans le navigateur |
| Google Analytics | seulement après consentement |
| Instagram, Discord | simples liens |

**Les accès n'ont jamais leur place dans le dépôt** – même les fichiers supprimés restent
lisibles dans l'historique. Ils vont dans un gestionnaire de mots de passe commun de
l'association, au minimum : owners/admins du dépôt, `MITGLIEDER_PASSWORT`, login Formspree
(quel ID pour quoi, quelle adresse destinataire), le jeton GitHub dans Formspree, admins
d'Instagram/Discord, registraire et accès du domaine `nc-wiki.ch`, la boîte
`sponsoring@nc-wiki.ch`.

---

## 21. Où s'arrête le simple remplissage ?

**À faire soi-même :** tout ce qui se décrit comme « mettre le champ X du fichier Y à la
valeur Z », où Y est l'un des fichiers cités ici.

**Demander de l'aide** (quelqu'un qui connaît Hugo/le web ou un assistant IA avec accès au
dépôt) :

- nouvelle sorte de page, section, formulaire ou élément interactif ;
- modifications sous `layouts/`, `assets/css/` ou `.github/workflows/` ;
- nouvelle police, nouveau favicon ;
- tout ce qui touche plusieurs endroits à la fois (variables de couleur,
  `data/testablauf.yaml`, `data/subtests.yaml`).
