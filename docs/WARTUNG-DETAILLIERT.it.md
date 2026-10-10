# Curare il sito – guida dettagliata

[Deutsch](WARTUNG-DETAILLIERT.md) · [Français](WARTUNG-DETAILLIERT.fr.md) · **Italiano**

I compiti quotidiani (testi, notizie, PDF, immagini, eliminare) sono nella
**[guida breve](WARTUNG.it.md)**. Qui c'è tutto il resto – dal menu alla pagina iniziale, al
team e al design fino alla tecnica. La maggior parte delle sezioni si fa nel browser su
github.com; dove serve un computer proprio o conoscenze di programmazione, è indicato.

I nomi di file, cartelle e campi restano in tedesco, perché sono i nomi reali nel
repository.

## Indice

1. [Struttura del progetto](#1-struttura-del-progetto)
2. [Pagine, menu e navigazione](#2-pagine-menu-e-navigazione)
3. [Cartelle Excel nel dettaglio](#3-cartelle-excel-nel-dettaglio)
4. [Editor web (Pages CMS) nel dettaglio](#4-editor-web-pages-cms-nel-dettaglio)
5. [Link, blocchi e contenuti programmati](#5-link-blocchi-e-contenuti-programmati)
6. [Pagina iniziale](#6-pagina-iniziale)
7. [Team e nuova stagione](#7-team-e-nuova-stagione)
8. [Sostegno, donazioni, sponsor](#8-sostegno-donazioni-sponsor)
9. [FAQ, Uniguide, subtest, nomi dei download](#9-faq-uniguide-subtest-nomi-dei-download)
10. [Modalità esame](#10-modalità-esame)
11. [Generatori di apprendimento e pagina Alpha](#11-generatori-di-apprendimento-e-pagina-alpha)
12. [Area membri](#12-area-membri)
13. [Moduli](#13-moduli)
14. [Impostazioni in hugo.toml](#14-impostazioni-in-hugotoml)
15. [Testi fissi (i18n)](#15-testi-fissi-i18n)
16. [Design: colori, carattere, logo, elenco delle sezioni](#16-design-colori-carattere-logo-elenco-delle-sezioni)
17. [Eliminare un'intera sezione](#17-eliminare-unintera-sezione)
18. [Automazioni (GitHub Actions)](#18-automazioni-github-actions)
19. [Verificare il sito](#19-verificare-il-sito)
20. [Servizi terzi e accessi](#20-servizi-terzi-e-accessi)
21. [Dove finisce il «semplice compilare»?](#21-dove-finisce-il-semplice-compilare)

---

## 1. Struttura del progetto

Il sito è costruito con [Hugo](https://gohugo.io/) a partire da file di testo. Ogni
modifica su `main` avvia una costruzione; uno o due minuti dopo la nuova versione è online
su GitHub Pages (`kroeppster.github.io/nc-wiki/`).

| Cartella / file | Contenuto | Da toccare? |
| --- | --- | --- |
| `content/de\|fr\|it/` | tutte le pagine, stessa struttura per lingua | sempre |
| `data/*.yaml` | elenchi: FAQ, università, subtest, svolgimento del test, sponsor, nomi dei download, contatto donazioni/sponsorizzazione, elenchi di parole | a volte |
| `assets/downloads/` | PDF elencati automaticamente | quando si carica |
| `assets/images/`, `static/images/` | immagini (copertine, loghi) o logo e grafiche fisse | a volte |
| `i18n/de\|fr\|it.yaml` | testi fissi (pulsanti, moduli, annunci) | raramente |
| `hugo.toml` | impostazioni (conto alla rovescia, Analytics, social) | raramente |
| `layouts/`, `assets/css/` | aspetto e logica | solo con conoscenze |
| `.github/workflows/` | automazioni | solo con conoscenze |
| `redaktion/` | deposito per le cartelle Excel caricate | quando si carica |
| `scripts/` | strumenti (cartelle, verifiche, immagini) | solo con conoscenze |
| `archetypes/`, `docs/vorlage-*.md` | modelli da copiare | come aiuto |

In ogni cartella sotto `content/`, **`_index.md`** è la pagina panoramica della cartella;
ogni altro file `.md` è una pagina singola. Una nuova sezione ha sempre bisogno prima di un
`_index.md` – senza, per Hugo la cartella non esiste.

Ogni file comincia con un'**intestazione** tra due righe `---` (titolo, descrizione, menu,
data …), seguita dal testo in Markdown (`**grassetto**`, `[link](/percorso)`, `- ` per gli
elenchi, `## ` per i sottotitoli).

**Lavorare in locale** (facoltativo): installare Hugo Extended (versione in
`.github/workflows/hugo.yml`), poi `npm install` e `hugo server -D` – il sito gira su
http://localhost:1313/. `npm run build` costruisce come su GitHub.

---

## 2. Pagine, menu e navigazione

### Campi importanti dell'intestazione

| Campo | Effetto |
| --- | --- |
| `title` | titolo della pagina |
| `description` | testo sotto il titolo in Google; max. ~160 caratteri |
| `draft: true` | la pagina non viene pubblicata |
| `date` | notizie e rapporti annuali: ordinamento |
| `featured_image`, `featured_image_alt` | immagine di copertina, vedi guida breve 6 |
| `menu` | voce di menu, vedi sotto |
| `aliases` | vecchi indirizzi che rimandano qui |
| `downloads` | elenco di PDF proprio (rapporti annuali) |
| `download_ordner` | elenco di PDF automatico da una cartella sotto `assets/` |
| `leer_hinweis: true` | la pagina elenco mostra una nota finché non ci sono sottopagine (rapporti annuali) |
| `geschuetzt: true` | protezione con password, vedi [12](#12-area-membri) |
| `layout` | modello particolare, p. es. `spenden` |

### Il menu

Il menu principale è composto **solo dalle intestazioni** – non esiste un file di menu.
Primo livello oggi: Pagina iniziale, News, EMS, Sostenitori e sostenitrici, Chi siamo,
Contatto.

```yaml
menu:
  main:
    parent: ueber-uns   # sotto quale voce
    weight: 5           # ordine, più piccolo = più avanti
    name: "Nome breve"  # facoltativo, altrimenti vale il title
```

- `parent` è il nome della cartella della sezione superiore (`ems`, `ueber-uns`,
  `unterstuetzer-innen`); senza `parent` la pagina diventa una voce di primo livello.
- `weight` può essere decimale (`2.5`) per inserire una voce tra due altre.
- Il blocco di menu deve stare in **ogni versione linguistica**.
- Il piè di pagina ha un proprio menu `legal` (impressum, privacy …), costruito allo stesso
  modo.
- I sottomenu si aprono con il mouse e al tocco; sul telefono solo al tocco. Niente da
  impostare.

### Rinominare o spostare una pagina

Cambia anche l'indirizzo. Perché i vecchi link funzionino ancora, nella **nuova**
posizione:

```yaml
aliases:
  - /vecchio/percorso/
```

I link interni al sito puntano nel vuoto finché non vengono adattati – la costruzione indica
ogni punto.

### Rapporto annuale e altri documenti singoli

1. Caricare il PDF in `static/downloads/jahresberichte/2027.pdf`.
2. Nuova pagina `content/it/ueber-uns/jahresberichte/2027.md` (modello:
   `archetypes/jahresbericht.md`):

   ```yaml
   ---
   title: "Rapporto annuale 2027"
   date: 2027-01-01
   downloads:
     - path: "downloads/jahresberichte/2027.pdf"   # relativo a static/
       label: "Rapporto annuale 2027 (PDF)"
   ---
   Due o tre frasi sull'anno.
   ```

   La dimensione del file viene aggiunta automaticamente. Lo stesso in DE e FR.

### Elenchi di PDF automatici

`download_ordner: "downloads/mitglieder"` nell'intestazione elenca tutti i PDF di
`assets/downloads/mitglieder/`. Esercizi, simulazioni e dispense hanno i loro elenchi
integrati. Per un nome più bello del nome del file: `data/downloads.yaml` (il formato è
spiegato lì, con traduzioni).

---

## 3. Cartelle Excel nel dettaglio

Procedura per la redazione: [guida breve 2](WARTUNG.it.md#2-modificare-i-testi-con-la-cartella-excel).

### Come nascono le cartelle

`.github/workflows/textmappen.yml` crea dopo ogni modifica su `main` tre cartelle
(`scripts/texte-ausgeben.py`) e le allega alla release GitHub **«Textmappen»** – di proposito
non sul sito. Non contengono bozze né pagine protette.

Struttura: foglio di istruzioni (nella lingua della cartella), foglio indice (link a ogni
pagina, contatore delle modifiche, descrizioni mancanti, colonne Responsabile/Stato/Nota),
poi un foglio per pagina nell'ordine della navigazione. Ogni foglio di pagina è una
**tabella Excel** con la colonna calcolata «Modifica» – se in Excel si inserisce una riga,
vi compare automaticamente «+ nuovo». (LibreOffice, Numbers e Google Fogli non lo
calcolano; il testo diventa comunque verde.) Colonne nascoste ricordano a quale paragrafo
appartiene una riga.

### Fogli «Vista» per pagina iniziale e team

I fogli «… – Vista» (linguetta arancione) sono costruiti come il sito: intestazione, tappe
della linea del tempo e riquadri affiancati, per il team una fila di schede per settore.
Solo le caselle bianche sono modificabili (protezione del foglio senza password).

- Team: scheda vuota = nuova persona, `!Eliminare!` nel nome = persona tolta, nel titolo del
  settore = settore intero tolto; in fondo due settori vuoti sono pronti.
- In FR/IT il testo tedesco è un commento sulla cella.
- Il team di ogni lingua si cura nella cartella di quella lingua.

Codice: `scripts/texte_ansicht.py`.

### Foglio Uniguide

«Uniguide – Vista» mostra l'intera tabella di `data/unis.yaml`: una riga per università,
una colonna per informazione. Quali colonne esistono, come si chiamano e dove compaiono è
definito in `data/uniguide-spalten.yaml` – e si modifica direttamente nel foglio:

- **Rinominare una colonna:** sovrascrivere il nome alla riga 4 (vale per la lingua della
  cartella; la piccola riga d'aiuto sotto può restare o sparire).
- **Eliminare una colonna:** `!Eliminare!` alla riga 4 – la colonna sparisce con tutti i
  valori. Le colonne di cui il sito ha bisogno (nome, lingua, EMS, corsi di laurea,
  bachelor/master a, sito, stato, fonte) si possono solo rinominare; lo dice il commento
  nell'intestazione.
- **Visualizzazione (riga 5):** *Tabella* = colonna nella grande tabella, *Pagina* = solo
  sulla pagina dell'università e nel confronto, *nascosto* = da nessuna parte (resta nella
  cartella).
- **Nuova colonna:** a destra ci sono tre colonne grigie vuote. Scrivere il nome alla riga 4
  e i valori sotto – ne nasce una nuova informazione (testo per lingua, sulla pagina
  dell'università sotto «Studio & sede»). Valori senza nome di colonna non vengono ripresi.
- **Intestazioni verdi**: testi per lingua, validi solo per la lingua della cartella. Se
  manca una traduzione, il sito mostra il testo tedesco. **Intestazioni scure**: valide per
  tutte le lingue.
- I valori sono testo libero – anche per i posti («non limitati (ca. 450 studenti)» è
  possibile). Più particolarità: una per riga. Elenchi (corsi di laurea, bachelor a, master
  a) separati da virgole. Lingue in qualsiasi grafia («tedesco, français»). EMS: ja / nein /
  teilweise (sì/no/in parte). Link con `https://`.
- Una casella vuota non elimina nulla, `!Eliminare!` svuota il campo. Le immissioni non
  valide non vengono riprese e sono segnalate nel rapporto.
- Alla lettura, in `data/unis.yaml` cambia solo quel campo; i commenti restano.
- Inserire solo ciò che figura su una pagina ufficiale, e modificare allora anche «Stato» e
  «Fonte». Una nuova università non si aggiunge tramite la cartella (vedi [9](#9-faq-uniguide-subtest-nomi-dei-download)).

Codice: `scripts/texte_uniguide.py`.

### Foglio Domande frequenti

«Domande frequenti – Vista» mostra tutte le domande di `data/faq.yaml`: una riga per domanda con
categoria, domanda, risposta, destinazione del link e testo del link.

- **Nuova domanda:** in basso ci sono cinque righe vuote. Scrivere domanda e risposta,
  scegliere la categoria dall'elenco (o scriverne una nuova). La domanda compare alla fine
  della sua categoria. Nelle altre lingue compare il testo tedesco fino alla traduzione –
  nella cartella FR/IT la riga è allora vuota e si può compilare.
- **Eliminare una domanda:** `!Eliminare!` nella casella «Domanda» – sparisce in tutte le
  lingue.
- **Destinazione del link:** percorso di una nostra pagina, p. es. `/ems/uniguide`, o un indirizzo completo con `https://` (p. es. Discord). Se la nostra
  pagina non esiste, il link non viene ripreso e lo si segnala.
- Le risposte sono testo semplice senza formattazione (finiscono anche nel blocco di dati
  per i motori di ricerca).

Codice: `scripts/texte_faq.py`.

### Cosa succede alla lettura

`.github/workflows/texte-einlesen.yml` legge le cartelle caricate con
`scripts/texte-einlesen.py`, costruisce il sito di prova e apre una pull request con un
rapporto. Ogni pagina modificata viene ricomposta dalle righe del suo foglio; i paragrafi
invariati restano identici carattere per carattere, le pagine invariate non vengono
toccate. Meglio un messaggio che un testo sbagliato:

| Caso | Cosa succede |
| --- | --- |
| La pagina è stata modificata altrove nel frattempo | pagina tralasciata, il resto arriva – riportare la modifica in una cartella recente |
| Stessa cartella caricata due volte | nessun danno («già ripreso») |
| Cella vuota / riga eliminata | il paragrafo resta – elimina solo `!Eliminare!` (anche `!Löschen!`, `!Supprimer!`) |
| Tabelle, blocchi, codice (grigio, corsivo) | restano invariati; si modificano nel file |
| Foglio ordinato | la pagina resta, messaggio |
| Celle spostate invece di righe intere | riconosciuto dalla formula di «Modifica»; la pagina viene ripresa come **appare**, ogni paragrafo sparito è nel rapporto |
| Riga copiata da un'altra pagina, riga grigia della pagina eliminata | riconosciuto e segnalato |
| Titolo e tutti i testi con `!Eliminare!` | la pagina viene eliminata |
| Eliminare una pagina ancora collegata | eliminata, il rapporto indica i link (altrimenti la costruzione diventa rossa) |
| Eliminare una pagina panoramica (`_index.md`) | solo se anche tutte le pagine sotto sono segnate |
| Pagina francese/italiana mancante | compilare il foglio → la pagina viene creata con l'intestazione di quella tedesca |
| Campo «nuova stagione» del foglio del team | cambio di stagione come in [7](#7-team-e-nuova-stagione) |

«Stato», «Nota» e «Responsabile» non vanno sul sito; il workflow li salva in
`redaktion/stand.json` (solo una somma di controllo per testo), la cartella successiva li
riprende.

### Da impostare una volta

*Settings → Actions → General → Workflow permissions → «Allow GitHub Actions to create and
approve pull requests»*. Altrimenti l'ultimo passaggio fallisce; il rapporto si trova allora
nel riepilogo dell'esecuzione. Una pull request aperta da un workflow non riceve la spunta
di `hugo.yml` (GitHub non lascia che un workflow ne avvii un altro) – perciò
`texte-einlesen.yml` costruisce da sé e scrive ✅/❌ nella pull request.

### Sul proprio computer

```bash
pip install openpyxl pyyaml
python3 scripts/texte-ausgeben.py --uebernehmen redaktion/stand.json   # tre cartelle
python3 scripts/texte-einlesen.py ncwiki-texte-it.xlsx --probe         # solo mostrare
python3 scripts/texte-einlesen.py ncwiki-texte-it.xlsx                 # scrivere
```

`--sprachen it` crea una sola cartella. Le cartelle non vanno nel repository
(`.gitignore`).

### Chi modifica gli script

La suddivisione di una pagina in paragrafi è definita una sola volta, in
`scripts/texte_bausteine.py`. Poi sempre **`python3 scripts/texte-mappe-pruefen.py`**:
lavora in una copia del progetto come una redattrice (modificare, inserire, spostare,
eliminare, fogli «Vista», nuova stagione, conflitti …), verifica ogni pagina e costruisce la
copia. Non tocca i file veri. Verifica anche le formule delle cartelle in Python
(riferimenti, intervalli, nessuna funzione più recente di Excel 2007). La colonna «Testo» è
formattata come testo, altrimenti Excel prenderebbe «- punto» per una formula.

---

## 4. Editor web (Pages CMS) nel dettaglio

Uso: [guida breve 3](WARTUNG.it.md#3-piccole-correzioni-nelleditor-web).

### Configurazione (una volta)

1. Accedere su [app.pagescms.org](https://app.pagescms.org) con GitHub.
2. *Install GitHub App* e autorizzare il repository `Kroeppster/nc-wiki`.
3. Aprire il repository, branch `main`. Le impostazioni sono in [`.pages.yml`](../.pages.yml).
4. Invitare chi scrive per e-mail sotto *Collaborators* – non serve un account GitHub.

### Cosa c'è – e cosa di proposito no

Per lingua: **pagine** (tutto l'albero), **notizie**, **resoconti**. Creare è possibile,
rinominare ed eliminare no (romperebbe dei link).

Non nell'editor: **area membri** e **Alpha** (un commento esplicativo nell'intestazione
andrebbe perso), **`data/*.yaml`** (pieni di commenti che l'editor cancellerebbe),
**caricare immagini**.

### Cosa cambia l'editor nei file

Al salvataggio Pages CMS riscrive tutto il file: le virgolette nell'intestazione
spariscono, i testi lunghi vengono spezzati, gli elenchi scritti uno sotto l'altro, `&`
diventa `&amp;`, le tabelle vengono riallineate. Per Hugo è lo stesso.
`scripts/editor-rundlauf.mjs` salva ogni pagina come fa Pages CMS, costruisce le due
versioni e confronta – l'ultima volta 440 pagine su 440 uguali. Le cartelle Excel se la
cavano con i testi spezzati.

### Chi modifica `.pages.yml`

- **`settings.content.merge: true` deve restare.** Altrimenti Pages CMS riscrive solo i
  campi nominati lì – menu, ordine, tag e la pagina iniziale (`hero`, `weg`, `material`)
  sparirebbero al primo salvataggio.
- Poi `node scripts/editor-rundlauf.mjs` (serve una volta qualche pacchetto npm in una
  cartella a parte, vedi l'intestazione dello script).
- Pages CMS rifiuta le chiavi sconosciute; i campi riutilizzati sono quindi ancore YAML
  (`&titel`, `*titel`) nella parte tedesca.

---

## 5. Link, blocchi e contenuti programmati

### Link interni

Link Markdown normali con il percorso, senza lingua né `/nc-wiki/`:
`[Uniguide](/ems/uniguide)`. L'hook `layouts/_default/_markup/render-link.html` ne fa
l'indirizzo giusto nella lingua della pagina e interrompe la costruzione se la
destinazione non esiste.

**Niente `{{< ref >}}` né altri shortcode nel testo.** L'editor web li rompe al
salvataggio – anche se qualcuno cambia solo una virgola sulla pagina.

### Blocchi

Blocco di codice con la lingua `baustein` (`layouts/_default/_markup/render-codeblock-baustein.html`):

| Nome | Cosa | Dati |
| --- | --- | --- |
| `testablauf` | tabella dello svolgimento | `data/testablauf.yaml` |
| `team-leitung` | schede del team dirigente | `ressorts:` nell'intestazione della pagina del team |
| `fakten-generator` | generatore di fatti | `data/fakten-generator/` |
| `figuren-generator` | generatore di figure | – |
| `sponsoring-kontakt` | pulsante e-mail/telefono | `data/sponsoring.yaml` |
| `antwortbogen-auswertung` | valutare il foglio delle risposte da foto (Alpha) | `data/antwortbogen.yaml` |
| `konztest-auswertung` | valutare il test di concentrazione da foto (Alpha) | `data/konztest.yaml` |

Un errore di battitura nel nome interrompe la costruzione. Nuovi blocchi: creare un partial
sotto `layouts/partials/bausteine/` e aggiungere il nome alla lista `$erlaubt` dell'hook.

### Mostrare qualcosa solo da una certa ora

```
{{< reveal-at when="2027-02-10T22:00:00+01:00" >}}
[Iscriviti ora](https://...)
{{< /reveal-at >}}
```

Il fuso orario è obbligatorio (`+01:00` inverno, `+02:00` estate); senza data valida il
contenuto resta nascosto. Il nascondere avviene solo nel browser – non adatto a cose
segrete. **Attenzione:** è uno shortcode. Poi non salvare più la pagina nell'editor web, e
togliere il blocco dopo la scadenza.

---

## 6. Pagina iniziale

La pagina iniziale è costruita dall'**intestazione** di `content/de|fr|it/_index.md`
(modello `layouts/index.html`). I testi si modificano più facilmente con il foglio
«… – Vista» della pagina iniziale nella cartella Excel; altrimenti nei tre file.

### Ordine delle sezioni

Hero → notizie → «Cosa ti serve e quando» (linea del tempo) → «Il materiale» → gli otto
subtest → missione → fascia del marchio → appello alle donazioni. Riordinare: spostare i
blocchi `<section>` in `layouts/index.html` e distribuire la classe `section-surface` in
modo che sezioni chiare e colorate si alternino.

### Hero

```yaml
hero:
  bild: "testsimulationen/testsimulation-2023.jpg"   # relativo a assets/images/
  bild_alt: "Aula piena durante una simulazione …"
```

`bild_alt` è obbligatorio appena c'è un'immagine (tradotto in ogni lingua). Senza `bild`
non compare nessuna foto. La foto deve mostrare che qui succede qualcosa di vero – niente
immagini simboliche.

### Linea del tempo (`weg:`)

```yaml
weg:
  start: "2026-10-01"            # inizio dell'asse
  ende: "2027-09-30"             # fine dell'asse
  termine:
    - wann: "Dez. bis 15. Feb."  # testo come mostrato
      titel: "Voranmeldung bei swissuniversities"
      von: "2026-12-01"          # determina la posizione sull'asse
      bis: "2027-02-15"          # vuoto = un solo giorno
      art: "offiziell"           # offiziell | angebot
      fuer: "mit"                # mit | ohne | beide (selettore con/senza EMS)
    - wann: "Februar bis Mai"
      titel: "Technik aufbauen"
      text: "…"                  # mostrato solo per l'offerta
      von: "2027-02-16"
      bis: "2027-04-30"
      art: "angebot"
      fuer: "beide"
      mittel:                    # link, solo per l'offerta
        - titel: "Uniguide"
          url: "ems/uniguide/"
```

Un asse del tempo continuo da ottobre a settembre: **ogni voce si colloca automaticamente dove
cade la sua data** (`von`/`bis`). In alto le date ufficiali di swissuniversities, sotto la
nostra offerta; i testi che si sovrapporrebbero passano da soli su un'altra riga. Un selettore
passa dalle date per le università con EMS a quelle senza (`fuer`). Nuova stagione: modificare
`start`, `ende` e gli anni delle date, nelle tre lingue. Tutto si trova nella cartella Excel,
foglio «Pagina iniziale – Vista», come tabella (una riga per voce; **nuove voci**: compilare una
delle righe vuote in basso, necessari titolo e inizio; eliminare con `!Eliminare!` nel titolo; link
«Titolo | ems/uniguide/», una riga per link). Codice: `scripts/texte_zeitstrahl.py`. Modificare le
date solo se così figurano presso swissuniversities. Su smartphone diventa un elenco verticale
per data. Calcolo: `layouts/partials/weg-positionen.html`, visualizzazione `weg-grid.html`.

### Riquadri del materiale (`material:`)

```yaml
material:
  items:
    - key: uebungsaufgaben        # non tradurre
      titel: "Serie di esercizi"
      zahlen: ["uebungen"]        # riempie {1}
      text: "{1} serie per tutti gli otto subtest, con soluzioni."
```

`key` ammessi: `uebungsaufgaben`, `testsimulationen`, `vorbereitungskurse`, `community`.

**Mai scrivere i numeri a mano.** `layouts/partials/angebot-zahlen.html` riconta a ogni
costruzione: serie senza i PDF delle soluzioni, simulazioni per annata, università e
domande dai file di dati, resoconti per lingua. Nel testo si mette `{1}`, `{2}` …

Le immagini di un riquadro sono definite in `layouts/partials/material-grid.html` (blocco
`$quellen`). Le pagine dei PDF sono sempre mostrate **intere** (`papier: true`, sfondo
bianco, `object-fit: contain`) – i PDF di origine sono in parte A4, in parte US Letter. Le
foto possono essere ritagliate. Un nome con estensione si cerca sotto `assets/images/`,
senza estensione sotto `assets/images/angebot/`. Rigenerare con
`python3 scripts/angebot-bilder-erzeugen.py` (serve `pip install pymupdf`; in cima allo
script ci sono PDF e pagina di ogni immagine). La scheda Discord di proposito non è un
finto screenshot.

Togliere o riordinare tappe e riquadri: eliminare o spostare la voce nei tre file. Un
riquadro del tutto nuovo richiede una voce in `$quellen` (passo di sviluppo).

Attenzione nel modello: un commento Hugo `{{/* */}}` dentro un `dict` rompe la costruzione.

---

## 7. Team e nuova stagione

### Team dirigente

Si trova nell'intestazione di `content/<lingua>/ueber-uns/team/_index.md` sotto
`ressorts:`; il blocco `team-leitung` ne fa le schede.

```yaml
ressorts:
  - titel: "Presidenza"
    mitglieder:
      - name: "Nome Cognome"
        rolle: "Co-presidente"
        foto: "team/nome-cognome.jpg"   # facoltativo, relativo a assets/images/
```

Ordine dei blocchi = ordine sulla pagina. Senza foto compare un cerchio colorato con le
iniziali. I nomi sono uguali in tutte le lingue, `titel` e `rolle` si traducono. Il modo
più semplice: il foglio «… – Vista» del team nella cartella Excel.

### Nuova stagione

Due strade che fanno la stessa cosa (`scripts/texte_saison.py`):

- nella cartella Excel, foglio «… – Vista» del team, compilare «Iniziare una nuova
  stagione» e caricare, **oppure**
- su GitHub *Actions → Neue Saison starten → Run workflow*, inserire la stagione (dà una
  pull request).

In tutte e tre le lingue la sezione «Team stagione …» passa, insieme a un elenco del team
dirigente, nell'archivio (`ueber-uns/archiv/`, in cima sotto le stagioni precedenti), e la
pagina del team inizia la nuova stagione con una frase provvisoria. Il team dirigente
stesso resta; i cambi si fanno dopo. Una seconda esecuzione con la stessa stagione non fa
nulla.

### Archivio

`content/<lingua>/ueber-uns/archiv/_index.md` è testo normale: stagioni precedenti, ex
responsabili, vecchie dispense (elenco automatico da `assets/downloads/archiv-kursskripte/`)
e sotto le vecchie notizie (`ueber-uns/archiv/news/`).

---

## 8. Sostegno, donazioni, sponsor

### «Sostienici ora»

`content/<lingua>/unterstuetzer-innen/jetzt-unterstuetzen.md` ha `layout: spenden`
(`layouts/_default/spenden.html`):

- il **primo** sottotitolo `##` con il suo testo sta a sinistra del grande codice TWINT,
  sotto il pulsante «Donare con bonifico»;
- il **secondo** sottotitolo `##` forma la parte sponsorizzazione con il pulsante
  «Ulteriori informazioni» (verso la pagina Sponsor).

I testi restano quindi testo normale (cartella, editor). Etichette dei pulsanti: `i18n`,
prefisso `spenden_`. Cambiare il codice TWINT: sostituire
`assets/images/unterstuetzen/twint-qr.png` (quadrato). Resta su fondo bianco anche in
modalità scura, perché l'app lo legga. Le coordinate bancarie sono su
`unterstuetzer-innen/spenden-ueberweisung.md`. Pagamento con carta non ancora disponibile.

### Pagina Sponsor

`unterstuetzer-innen/sponsoren.md` è testo normale; alla fine c'è il blocco
`sponsoring-kontakt`. E-mail e telefono in `data/sponsoring.yaml` – se `telefon` è vuoto,
non compare il pulsante del telefono.

### Loghi degli sponsor

I loghi su «Sostenitori e sostenitrici» vengono da `data/sponsors.yaml` (spiegato campo per
campo nel file):

1. Caricare il logo in `assets/images/sponsors/` (preferibilmente SVG).
2. Aggiungere una voce:

   ```yaml
   - name: "Nome dell'azienda"
     logo: "file.svg"
     website: "https://esempio.ch/"
   ```

Ordine nel file = ordine dei riquadri. Togliere: eliminare la voce. I loghi scuri ricevono
automaticamente uno sfondo chiaro (`.sponsor-logo`).

---

## 9. FAQ, Uniguide, subtest, nomi dei download

### FAQ (`data/faq.yaml`)

Il modo più semplice: il foglio «Domande frequenti – Vista» della cartella Excel ([3](#3-cartelle-excel-nel-dettaglio)). Nel file:

```yaml
- id: "identificativo-unico"
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

La pagina raggruppa per categoria, nell'ordine del file. La domanda «Quali subtest ci
sono?» aggiunge automaticamente l'elenco di `data/subtests.yaml` (`dynamic: subtests`); la
frase che precede («9 subtest») è fissa nella FAQ.

### Uniguide (`data/unis.yaml`, `data/uniguide-spalten.yaml`)

I valori stanno in `data/unis.yaml`; quali informazioni esistono, come si chiamano, se
compaiono come colonna della tabella, solo sulla pagina dell'università o da nessuna parte,
e in quale sezione della pagina, sta in `data/uniguide-spalten.yaml` (descrizione dei campi
in testa al file). Tabella, confronto e pagina dell'università si costruiscono da soli – una
nuova colonna non richiede codice. Ogni università ha bisogno in più di una pagina quasi
vuota `content/<lingua>/ems/uniguide/<slug>.md` con `title` e `uni_slug`. Il modo più
semplice per modificare: il foglio «Uniguide – Vista» della cartella Excel ([3](#3-cartelle-excel-nel-dettaglio)).

Un valore semplice (`semestergebuehr: "CHF 850"`) vale per tutte le lingue, altrimenti per
lingua (`de:`/`fr:`/`it:`). I nomi delle lingue d'insegnamento vengono da `i18n`
(`sprache_…`). «Sede di studio» è la città; il vantaggio del domicilio ha una colonna
propria; «Bachelor a» e «Master a» indicano dove si studiano i due livelli.

**Niente stime.** Un campo resta `null` finché il valore non figura su una pagina
ufficiale – allora modificare anche `stand` (data) e `quelle` (link). I posti provengono
dalle capacità d'accoglienza di swissuniversities (indicazione della fonte nel campo
`hinweis` della colonna). I campi vuoti non compaiono; le colonne con `fehlt: true`
figurano allora nel riquadro «Queste informazioni mancano ancora» della pagina
dell'università.

`berichte_ort` deve corrispondere esattamente all'`ort:` dei resoconti; allora i tre più
recenti compaiono sulla pagina dell'università. Il confronto permette fino a quattro
università affiancate (`var MAX = 4` in `layouts/partials/uniguide-table.html`).

### Subtest (`data/subtests.yaml`)

Alimenta i riquadri dei subtest. **L'ordine = l'ordine nel giorno del test** e deve
corrispondere a `data/testablauf.yaml`. `slug` = nome della cartella sotto
`content/<lingua>/ems/uebungsaufgaben/`; `number` non viene mostrato. Riordinando, adattare
anche il `weight` delle pagine di esercizi. Il sito ha 8 pagine di esercizi, perché
«Figure e fatti» riunisce due subtest ufficiali – il vero EMS ne ha 9.

Un'indicazione in più accanto ai download di una pagina di esercizi:
`downloads_notice: "Nuovo layout!"` nell'intestazione (per lingua).

### Nomi dei download (`data/downloads.yaml`)

Le serie di esercizi e le simulazioni del test compaiono raggruppate per anno (il più
recente è aperto). Per le serie la dicitura («Serie 2», pulsanti «Esercizi» e «Soluzione») nasce
automaticamente dal nome del file. Se la soluzione è nello stesso PDF, il nome del file va
sotto `mit_loesung:` – il pulsante si chiama allora «Esercizi con soluzione». Tutti gli altri
file (fascicoli del test, valutazioni, dispense) ricevono sotto `overrides:` un nome con
traduzioni, per le simulazioni del test senza l'anno. Il formato è spiegato in testa al file.

---

## 10. Modalità esame

`/ems/pruefungsmodus/`: legge ad alta voce le istruzioni, mostra un orologio a schermo
intero e dice «Stop» – per un subtest o per tutto il giorno senza pause. Gli esercizi
vengono dai PDF.

### Durate e ordine

Tutto in **`data/testablauf.yaml`**: blocchi nell'ordine del giorno del test con `minuten`,
numero di esercizi, punti e nomi nelle tre lingue. Il file alimenta la tabella su `/ems/`
(blocco `testablauf`), la modalità esame e le durate predefinite dei generatori. Il tempo
totale viene sommato. **Modificare con cura** – un numero sbagliato significa mesi di
esercizio con la durata sbagliata.

### Svolgimento personalizzato

- **Normale:** scegliere subtest e numero di esercizi; il tempo si calcola al ritmo del
  vero EMS (7 esercizi «Muster zuordnen» = 6:13). Internamente si calcola in **secondi**.
- `aufgaben_fest: true` (memorizzare figure/fatti): lì è regolabile il **tempo** invece del
  numero.
- **Modalità esperto:** minuti e pause liberi. Un link condiviso che ne ha bisogno la
  attiva da sé. Formato del tempo nel link `6m13` (un numero solo vale come minuti, i
  vecchi link restano validi).
- La composizione si condivide tramite link; nulla viene salvato su un server.

### Annunci

Testi in `i18n/*.yaml`, prefisso `pm_` – brevi, senza parentesi né abbreviazioni, perché
vengono pronunciati. Forma di cortesia, come un·a sorvegliante. Per DE e FR ci sono 15
registrazioni sotto `assets/audio/pruefungsmodus/<lingua>/` (elenco nel README; voce
francese CC-BY 4.0, attribuzione nel README); una registrazione ha la precedenza sulla
sintesi vocale del browser. In italiano legge il dispositivo. Dopo una modifica a un testo
`pm_`, eliminare la registrazione o rigenerarla con `scripts/ansagen-erzeugen.py`.
Registrazioni vere dell'associazione: sovrascrivere il file con lo stesso nome.

### Tecnica da conoscere

- L'orologio memorizza un'**ora di fine** invece di contare i secondi (i browser rallentano
  le schede in secondo piano).
- Wake-Lock tiene acceso lo schermo; lo schermo intero è solo un extra.
- Nessuna attesa tra i blocchi, nessuna ora di fine mostrata, la pausa è indicata come
  «solo per esercitarsi».
- Numero di esercizi/tempo modificato → la frase viene letta invece della registrazione
  (che cita i valori veri). `{dauer}` usa `pm_dauer_min`/`pm_dauer_min_sek`.
- Non togliere `safeJS` in `layouts/partials/pruefungsmodus.html` – altrimenti la pagina
  resta muta.

---

## 11. Generatori di apprendimento e pagina Alpha

Il materiale per «Figure e fatti» serve una volta sola – due generatori creano quindi
sempre nuovi set. Entrambi si svolgono a schermo con orologio o si stampano come fascicolo
di sei pagine (istruzioni, pagina da memorizzare, domande, foglio risposte, soluzioni;
intestazione, numero di pagina, logo CC-BY-NC). Durate e pausa (il vero intervallo nel
giorno del test) vengono da `data/testablauf.yaml`.

**Stato attuale:** per ora i due generatori si trovano solo sulla
[pagina Alpha](#pagina-alpha) (`content/de/alpha/_index.md`), non sulla pagina pubblica
«Figure e fatti». Per approvarli, rimettere il blocco nel testo della pagina degli esercizi
(nelle tre lingue, con il rimando al generatore in «Tranelli tipici»).

### Formato del fascicolo

Misure prese dallo **strumento di formattazione NCWiki** privato (`vorlage/ems.typ`).
Cornice comune: `layouts/partials/bausteine/ems-heft.html`, stili in `assets/css/style.css`
(«EMS-Heft»). Modificare una misura prima nello strumento, poi riprendere lo stesso numero.
**Riprendere solo il formato, mai i contenuti** – lo strumento è privato, il sito pubblico.
Prima di toccare le regole di stampa, leggere il commento presso `@media print` (le pagine
del fascicolo vanno in un contenitore a parte sotto `<body>`; regole legate a
`body.fg-druckt`).
Stato: `ems.typ` dopo l'allineamento ai file InDesign del Probelauf 2026 (margini 15 mm,
prima linea di base 98.66, riquadro, freccia e STOP, griglia delle figure, domande sui fatti
su due colonne in posti fissi, chiave di correzione). Le istruzioni seguono il testo del
fascicolo ufficiale in `i18n` (`fg_anl_*`, `fig_anl_*`, `ems_*`). Per verificare: stampare
un set («Salva come PDF») e confrontare la posizione di testi e linee con il foglio dello
strumento (p. es. con `pymupdf`); scarti tollerati sotto 1 pt (il browser arrotonda ai pixel).

### Generatore di fatti

Elenchi di parole in `data/fakten-generator/<lingua>.yaml` (per ora solo `de.yaml`; appena
esiste un `fr.yaml`/`it.yaml`, compare da solo). Non sciogliere le categorie: una vera serie
dà a ogni fascia d'età tre professioni di **un** campo e tre malattie di **tre** tipi. Le
domande nascono da modelli di frase (`fragen`), più `namensgruppen`, `dativ`,
`nicht_attributiv`. `scripts/fakten-listen-auslesen.py` estrae parole dai PDF ma non
sovrascrive lo YAML. In sospeso: categorie non ancora approvate da una persona; ~40 invece
di ~80 voci per categoria.

**Gestione con Excel** (file a sé, non le cartelle di testi): `ncwiki-wortliste-fakten-generator.xlsx`,
sempre aggiornato sotto *Releases → Textmappen* (https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-wortliste-fakten-generator.xlsx).
Un foglio per elenco (Namensgruppen, Einzelne Namen, Berufe, Krankheiten, Merkmale, Dativ-Plural), più
«Anleitung» e «Übersicht» (conta con formule se le quantità minime sono raggiunte). Modificare, salvare,
caricare in `redaktion/` (il nome inizia con `ncwiki-wortliste`): `wortliste-einlesen.yml` controlla il file con
`scripts/wortliste.py` e apre una pull request con rapporto (nuovo / rimosso / avvisi). **In caso di errore**
non viene accettato nulla e non si apre nessuna pull request; l'esecuzione diventa rossa e il suo riepilogo
nomina ogni errore con foglio e riga (troppe poche parole, parola doppia, sesso diverso da m/w, caratteri
`< > & { }`). Quantità minime: 15 nomi singoli; almeno 5 campi professionali con almeno 3 professioni
ciascuno; almeno 3 tipi di malattia e 15 malattie; almeno 15 caratteristiche in minuscolo. L'Excel sostituisce
l'elenco **intero** (istantanea); se si basa su uno stato più vecchio, il rapporto avvisa. Si sostituiscono solo
i blocchi di parole – il commento esplicativo, i gruppi d'età e i modelli di domanda restano. Un nuovo campo o
tipo nasce inserendo un nuovo nome (corto, minuscolo, senza spazi; «Technik und Bau» darebbe un NUOVO campo
`technik_und_bau`, quindi usare l'elenco a tendina). In locale: `python3 scripts/wortliste.py ausgeben` oppure
`einlesen FILE [--probe]`; dopo modifiche allo script `python3 scripts/wortliste-pruefen.py`.

### Generatore di figure

Nessun file di dati, etichette in `i18n` (prefisso `fig_`). Ogni **serie** estrae prima il
suo stile (angoli, frastagliatura, grandezza, costruzione libera/mozzo/fasce), le 18 figure
lo seguono – altrimenti tutte le serie si somiglierebbero. Misurare invece di stimare:
`python3 scripts/figuren-vergleichen.py 14 [--original <PDF>]` (serve `pymupdf numpy scipy
pillow`; il PDF di esempio ufficiale di swissuniversities non è nel repository). Prima di
toccare il disegno, leggere l'intestazione di commenti di
`layouts/partials/bausteine/figuren-generator.html` – lì ci sono gli errori passati
(identificativi di clip doppi, campi che si frammentano, contorni levigati separatamente,
lettere nel baricentro, logo misurato come figura).

### Pagina Alpha

`content/de/alpha/` è il banco di lavoro per le nuove funzioni: protetta da password, non
collegata da nessuna parte, **solo in tedesco**. Una sezione per funzione, che dice cosa
valutare. Una volta approvata, il blocco passa sulla pagina vera (allora in tre lingue).
Attualmente: generatore di figure, generatore di fatti, «Antwortbogen auswerten» e «Konzentrationstest auswerten».

### Valutare il foglio delle risposte (Alpha)

Una foto del foglio delle risposte compilato di una simulazione viene letta nel browser e
confrontata con le soluzioni – la foto non lascia il dispositivo. Il procedimento è quello
dello strumento di formattazione (`werkzeug/auswertung.py`), trasposto in JavaScript
(`layouts/partials/bausteine/antwortbogen-auswertung.html`, leggere il commento in testa; la
parte comune – immagine, caricamento, PDF, fotocamera dal vivo – è in
`bausteine/bild-lesen.html`). La **fotocamera dal vivo** cerca i quattro angoli neri già nel
mirino e scatta da sola appena il foglio è fermo; altrimenti resta «Scatta una foto» (app
fotocamera).
Tutte le simulazioni dal 2022 hanno lo stesso foglio. Le soluzioni sono in
`data/antwortbogen.yaml` e **non si modificano a mano**: per una nuova simulazione caricare
come sempre il PDF delle soluzioni, inserirlo in `scripts/antwortbogen-loesungen.py` e
lanciare `python3 scripts/antwortbogen-loesungen.py --schreiben` (si interrompe se non trova
esattamente 144 soluzioni). Per le simulazioni che non sono sul sito c'è «Eigener
Lösungsschlüssel»: il PDF delle soluzioni dello strumento (o una foto della pagina con la chiave
di correzione) viene letto come un foglio compilato, le caselle nere sono le soluzioni; le
righe senza casella non contano. I PDF vengono aperti da pdf.js in `static/vendor/pdfjs/`
(volutamente non da una CDN: nulla deve lasciare il dispositivo; per aggiornarlo sostituire i
due `.mjs` del pacchetto npm `pdfjs-dist`). Dopo modifiche alla lettura: `python3
scripts/antwortbogen-testbilder.py /tmp/ab` (foto di prova con crocette note) e
`node scripts/antwortbogen-pruefen.mjs /tmp/ab`.

### Valutare il test di concentrazione (Alpha)

Come il foglio delle risposte, ma con il procedimento di `werkzeug/konztest_auswertung.py`: il
foglio non ha marche di riferimento, la griglia dei 1600 simboli fa essa stessa da riferimento
(macchie magenta → griglia → posizione dalla somiglianza dei simboli uguali → trasformazione
→ inchiostro per simbolo). Conteggio secondo le istruzioni: giusti meno sbagliati meno simboli
bersaglio omessi prima dell'ultimo segnato (valore grezzo); una barra viola indica quest'ultimo.
Toccare l'immagine inverte un segno. Inchiostro per simbolo: quanto è più scuro della carta subito
accanto (così le ombre non disturbano), meno ciò che lo stesso simbolo senza segno ha nello stesso
punto. La soglia «segnato» si ricava da ogni immagine; se i tratti non si distinguono chiaramente
(troppi casi dubbi, riflessi), la pagina chiede una nuova foto invece di un risultato incerto. Partial `layouts/partials/bausteine/konztest-auswertung.html`. Griglia, posizione e
soluzione in `data/konztest.yaml`, generato da `python3 scripts/konztest-loesungen.py
--schreiben` dal fascicolo (simboli come carattere 0–F) e dal PDF delle soluzioni (caselle
nere), con controprova sulla regola delle istruzioni. **Per ora solo 2026**: il 2022 ha cifre
come testo (soluzione deducibile dalla regola), il 2023 immagini con una mappa delle soluzioni
leggibile, il 2024/2025 solo immagini senza mappa. Verificare: `python3
scripts/konztest-testbilder.py /tmp/kt` e `node scripts/konztest-pruefen.mjs /tmp/kt`.

---

## 12. Area membri

`content/<lingua>/mitglieder/` – non nel menu, cifrata con password alla pubblicazione
(StatiCrypt, `scripts/encrypt-protected-pages.mjs`).

### Cosa offre la protezione

Tiene lontani motori di ricerca e visite casuali, ma **non è un login**: una password
comune; la pagina cifrata è pubblica e può essere attaccata offline; **i PDF collegati non
sono protetti** (chi conosce l'indirizzo può scaricarli). Quindi solo cose interne senza
rischi – niente dati personali, estratti conto, candidature.

### Nuova pagina protetta

Come ogni pagina, in più `geschuetzt: true` nell'intestazione (in tutte e tre le lingue).
Questo mette `noindex`, toglie la pagina da ricerca, sitemap e RSS e la cifra. Elenco di
PDF: `download_ordner: "downloads/mitglieder"`.

### Password

- Vale **due ore** dall'ultimo accesso, per tutte le pagine membri e lingue
  (`MERKDAUER_MINUTEN` in `scripts/passwort-vorlage.html`). Il browser conserva un valore di
  controllo con sale, non la password. Uscire: aggiungere `?staticrypt_logout`
  all'indirizzo.
- **Cambiare:** *Settings → Secrets and variables → Actions →* `MITGLIEDER_PASSWORT` →
  nuova password (almeno 16 caratteri casuali) → poi *Actions → Deploy Hugo site to GitHub
  Pages → Run workflow*. Nuova password nel gestore di password e ai membri. Il `SALZ` dello
  script resta.
- **Costruzione rossa con «Kein Passwort gesetzt»:** manca il secret – la costruzione si
  interrompe di proposito invece di pubblicare in chiaro. Per le pull request solo un
  avviso.
- In locale: `npm run build && STATICRYPT_PASSWORD='test' npm run schuetzen`, risultato in
  `public/mitglieder/`.

---

## 13. Moduli

Il sito non ha un server; i moduli passano per **Formspree**.

| Modulo | Dove | ID Formspree | File |
| --- | --- | --- | --- |
| Contatto | `/kontakt/` | `mvkpgrpl` | `layouts/partials/contact-form.html` |
| Segnalare un errore (esercizi) | pagine degli esercizi | anche `mvkpgrpl` | `layouts/partials/report-error-general.html` |
| Resoconto | `/ems/erfahrungsberichte/` | `xaewqwoj` | `layouts/partials/experience-form.html` |

Le segnalazioni finiscono provvisoriamente nella casella dei contatti, con l'oggetto fisso
«Fehlermeldung Uebungsaufgaben (Website)» per filtrare. Indirizzo proprio più avanti:
inserirlo solo in `report-error-general.html`.

**Non cambiare l'indirizzo dei resoconti:** un invio avvia tramite `repository_dispatch` il
workflow `erfahrungsbericht-intake.yml`, che crea file e pull request (il token GitHub
necessario è salvato solo in Formspree).

L'invio in background è gestito da uno script comune in `layouts/partials/footer.html` per
tutti i moduli con la classe `report-error`. Un nuovo modulo in un nuovo punto è un passo
di sviluppo.

---

## 14. Impostazioni in hugo.toml

Sotto `[params]`:

| Campo | Effetto |
| --- | --- |
| `ems_exam_date = '2027-07-09T08:00:00+02:00'` | obiettivo del conto alla rovescia sulla pagina iniziale (fuso orario obbligatorio) |
| `google_analytics_id` | Google Analytics; vuoto = disattivato |
| `social_instagram`, `social_discord`, `social_linkedin` | pulsanti nel piè di pagina; vuoto = nessun pulsante |
| `newsletter_url` | iscrizione alla newsletter; vuoto = nessun blocco newsletter |

Google Analytics si carica **solo** se nel banner dei cookie è stato scelto «Accetta».
Testi del banner: `i18n`, prefisso `cookie_`.

---

## 15. Testi fissi (i18n)

`i18n/de.yaml`, `fr.yaml`, `it.yaml` contengono tutti i testi che non appartengono a una
pagina: pulsanti, moduli, banner dei cookie, annunci, etichette. A sinistra la chiave, a
destra il testo; **i tre file hanno le stesse chiavi**. Modificare un testo sempre nei tre
file. Una nuova chiave ha effetto solo se viene usata in `layouts/`.

---

## 16. Design: colori, carattere, logo, elenco delle sezioni

### Colori

Tutto in `assets/css/style.css`, in alto come variabili. Ci sono **due palette**:
`:root{…}` (chiara) e `:root[data-theme="dark"]{…}` (scura) – modificare un colore sempre in
entrambe.

- `--color-signal` è il colore dei link e del marchio, `--color-btn-bg` lo sfondo dei
  pulsanti pieni. In modalità scura differiscono di proposito (link chiaro, ma contrasto
  sufficiente per il testo bianco dei pulsanti) – adattare entrambi.
- `--cta-from`/`--cta-to` e `--color-avatar-0…5` esistono solo in chiaro, perché ci sta
  sopra testo bianco – non renderli mai troppo chiari.
- Profondità: `--shadow-sm|md|lg`, `--glow-*`, `--band-*`, `--color-section-alt`. Le ombre
  sono più forti in modalità scura.
- Prima di ogni cambio di colore verificare il contrasto («WCAG contrast checker»): testo
  4.5 : 1, titoli grandi 3 : 1, in entrambe le modalità.

### Carattere

**Poppins** (titoli) e **Inter** (testo), serviti da `static/fonts/` (non caricati da
Google – protezione dei dati). Sostituire: mettere lì il `.woff2` **e** adattare il blocco
`@font-face` e `--font-display`/`--font-body`.

### Logo e favicon

Logo: `static/images/logo.svg` (intestazione, hero, fascia del marchio). È disegnato scuro e
diventa bianco tramite filtro in modalità scura e nella fascia scura (`--logo-filter`,
`.brand-band-logo`). Un nuovo logo multicolore ha bisogno di una soluzione propria. Il
favicon (`static/favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`) non viene generato
automaticamente – con un nuovo logo rifarlo con uno strumento per immagini o favicon e
caricarlo con gli stessi nomi.

### Elenco delle sezioni («In questa pagina»)

Nasce automaticamente dai sottotitoli `##` (da due in su). Da 1100 px a destra del testo,
sotto chiuso sopra il testo. Codice: `layouts/partials/seiten-uebersicht.html`, griglia
`.seite-raster`/`.mit-liste` in `single.html`/`list.html`, etichetta `auf_dieser_seite`. Non
tornare a: blocco tra titolo e testo, barra che appare solo scorrendo, fila orizzontale che
scorre. Lo script aspetta `DOMContentLoaded`, raccoglie anche i titoli che vengono dai
modelli, prende spazio dal margine (`--rand-ausbruch`) e ha bisogno di
`--sprung-abstand`/`--kopf-hoehe` perché le ancore non finiscano sotto l'intestazione.

---

## 17. Eliminare un'intera sezione

- Eliminare `_index.md` e tutte le pagine sotto, **in tutte e tre le lingue**. La voce di
  menu sparisce con esse.
- La costruzione resta rossa finché dei link puntano alla sezione – adattare quei punti.
- PDF e immagini sotto `assets/` o `static/` non vengono eliminati insieme.
- Alternativa nella cartella Excel: segnare titolo e tutti i testi con `!Eliminare!`.

---

## 18. Automazioni (GitHub Actions)

| Workflow | Quando | Cosa |
| --- | --- | --- |
| `hugo.yml` | ogni modifica a `main`, ogni pull request | costruire, ricerca (Pagefind), verificare i link interni (blocca), link esterni (avviso), cifrare l'area membri, pubblicare (solo `main`) |
| `textmappen.yml` | ogni modifica a `main` | cartelle Excel recenti nella release «Textmappen» |
| `texte-einlesen.yml` | cartella caricata in `redaktion/` | leggere, costruire di prova, pull request con rapporto |
| `wortliste-einlesen.yml` | `ncwiki-wortliste*.xlsx` caricato in `redaktion/` | controllare, leggere, costruire di prova, pull request con rapporto; in caso di errore nessuna pull request, esecuzione rossa |
| `neue-saison.yml` | a mano (*Run workflow*) | cambio di stagione come pull request |
| `erfahrungsbericht-intake.yml` | invio Formspree | nuovo resoconto come pull request |

Una costruzione fallita non mette il sito offline; resta l'ultima versione buona. Versione
di Hugo: fissata in `hugo.yml` – aumentandola, testare anche in locale.

---

## 19. Verificare il sito

La costruzione verifica da sé i link interni. In più ci sono script di verifica (in locale,
con il sito costruito sotto `public/`):

```bash
npm run build
npx http-server public -p 8099 -s &
BREITEN=1280,768,390 MODI=light,dark node scripts/seiten-pruefen.mjs  # layout, contrasto, immagini
python3 scripts/struktur-pruefen.py                                  # doppioni, pagine irraggiungibili, link morti
npx pagefind --site public && node scripts/verhalten-pruefen.mjs     # uso, moduli (Formspree intercettato)
node scripts/fakten-generator-pruefen.mjs                            # 150 set + PDF
node scripts/figuren-generator-pruefen.mjs                           # 12 set + PDF
python3 scripts/antwortbogen-testbilder.py /tmp/ab && node scripts/antwortbogen-pruefen.mjs /tmp/ab  # foto di fogli
python3 scripts/konztest-testbilder.py /tmp/kt && node scripts/konztest-pruefen.mjs /tmp/kt              # foto del test di concentrazione
python3 scripts/texte-mappe-pruefen.py                               # cartelle Excel
python3 scripts/wortliste-pruefen.py                                 # elenco di parole (Excel)
node scripts/editor-rundlauf.mjs                                     # editor web
```

Altra porta: `ADRESSE=http://127.0.0.1:8123` davanti. Atteso: esattamente dieci pagine
irraggiungibili (area membri e Alpha). Provare una nuova verifica prima su un errore vero e
noto, e togliere i falsi allarmi – altrimenti presto nessuno la legge più.

---

## 20. Servizi terzi e accessi

| Servizio | Per cosa |
| --- | --- |
| GitHub Pages / Actions | hosting e automazione. Il passaggio a `nc-wiki.ch` è preparato ma non attivo (nessun `CNAME`, DNS non cambiato). |
| Formspree | moduli ([13](#13-moduli)) |
| Pages CMS | editor web ([4](#4-editor-web-pages-cms-nel-dettaglio)) |
| Pagefind | ricerca, gira tutta nel browser |
| Google Analytics | solo dopo consenso |
| Instagram, Discord | solo link |

**Gli accessi non vanno mai nel repository** – anche i file eliminati restano leggibili
nella cronologia. Vanno in un gestore di password comune dell'associazione, almeno:
owner/admin del repository, `MITGLIEDER_PASSWORT`, login Formspree (quale ID per cosa, quale
indirizzo destinatario), il token GitHub in Formspree, admin di Instagram/Discord,
registrar e accesso del dominio `nc-wiki.ch`, la casella `sponsoring@nc-wiki.ch`.

---

## 21. Dove finisce il «semplice compilare»?

**Da fare da sé:** tutto ciò che si descrive come «impostare il campo X del file Y sul
valore Z», dove Y è uno dei file citati qui.

**Chiedere aiuto** (qualcuno che conosce Hugo/il web o un assistente IA con accesso al
repository):

- nuovo tipo di pagina, sezione, modulo o elemento interattivo;
- modifiche sotto `layouts/`, `assets/css/` o `.github/workflows/`;
- nuovo carattere, nuovo favicon;
- tutto ciò che tocca più punti insieme (variabili di colore, `data/testablauf.yaml`,
  `data/subtests.yaml`).
