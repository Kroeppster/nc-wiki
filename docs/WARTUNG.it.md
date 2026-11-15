# Curare il sito – guida breve

[Deutsch](WARTUNG.md) · [Français](WARTUNG.fr.md) · **Italiano**

Qui c'è solo il lavoro di tutti i giorni: modificare testi, scrivere una notizia, caricare
PDF e immagini, eliminare qualcosa. Tutto si fa nel browser, non serve installare nulla.
Tutto il resto (pagina iniziale, team, menu, design, moduli, area membri, tecnica) si
trova nella **[guida dettagliata](WARTUNG-DETAILLIERT.it.md)**.

I nomi di file e cartelle (`content/de/…`, `redaktion/` …) restano in tedesco, perché sono
i nomi reali nel repository.

---

## Prima di iniziare

**Che cosa ti serve**

- Un account gratuito su [github.com](https://github.com) e un invito al repository
  `Kroeppster/nc-wiki`. L'invito lo dà chi si occupa del sito; senza, puoi leggere tutto
  ma non modificare nulla.
- Per la cartella Excel: Excel.
- Nient'altro. Non devi installare programmi né saper programmare.

**Non puoi rompere quasi nulla.** GitHub conserva per ogni modifica lo stato precedente;
lo si può recuperare ([sezione 12](#12-controllare-e-annullare)). Se la verifica
automatica trova un errore nella tua modifica, il sito di prima resta semplicemente
online.

**Le parole che ricorrono sempre**

| Parola | Che cosa significa |
| --- | --- |
| repository | la cartella con tutti i file del sito, su GitHub |
| `main` | lo stato valido. Ciò che sta su `main` viene pubblicato |
| commit, «Commit changes» | salvare. Ogni modifica salvata riceve una breve descrizione, così gli altri vedono che cosa è cambiato |
| pull request | una proposta di modifica, non ancora valida (così arrivano le cartelle Excel) |
| merge | accettare la proposta. Solo dopo è su `main` |
| costruzione, «Actions» | dopo ogni salvataggio GitHub ricostruisce il sito e lo verifica. Spunta verde: online. Croce rossa: [sezione 10](#10-quando-la-costruzione-è-rossa) |
| Markdown, `.md` | semplici file di testo da cui nascono le pagine ([sezione 14](#14-aiuto-per-scrivere)) |
| intestazione della pagina | le righe tra i due `---` in cima a un file `.md`: titolo, data, descrizione |

**Gli indirizzi:** sito [kroeppster.github.io/nc-wiki](https://kroeppster.github.io/nc-wiki/it/) ·
file [github.com/Kroeppster/nc-wiki](https://github.com/Kroeppster/nc-wiki) ·
editor web [app.pagescms.org](https://app.pagescms.org)

---

## 1. Quale strumento per cosa

| Vuoi … | Strumento | Sezione |
| --- | --- | --- |
| rileggere molti testi, tradurre, modificare la pagina iniziale o il team | **cartella Excel** | [2](#2-modificare-i-testi-con-la-cartella-excel) |
| correggere in fretta un errore su una pagina | **editor web** (Pages CMS) | [3](#3-piccole-correzioni-nelleditor-web) |
| scrivere una notizia | editor web o GitHub | [4](#4-scrivere-una-notizia) |
| caricare un PDF o un'immagine, eliminare un file | **GitHub** | [5](#5-caricare-un-pdf) – [8](#8-eliminare-un-file-o-una-pagina) |
| modificare una pagina esistente direttamente su GitHub | **GitHub** | [11](#11-modificare-un-file-direttamente-su-github) |
| vedere se la modifica è online, o annullare qualcosa | **GitHub** | [12](#12-controllare-e-annullare) |
| cambiare la data del prossimo AMS, passare il sito al nuovo anno | diversi | [13](#13-lista-di-controllo-per-il-nuovo-anno) |
| sapere come scrivere in grassetto, fare un elenco o un link | – | [14](#14-aiuto-per-scrivere) |

Tutti gli strumenti modificano gli stessi file. Dopo ogni modifica su `main`, GitHub
ricostruisce il sito; è online uno o due minuti dopo.

---

## 2. Modificare i testi con la cartella Excel

C'è **una cartella per lingua** (DE, FR, IT) con tutti i testi visibili del sito – ogni
pagina su un proprio foglio, all'inizio le istruzioni e un indice.

1. **Prendere una cartella recente:** su GitHub, a destra sotto *Releases → Textmappen*,
   oppure direttamente:
   [DE](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-de.xlsx) ·
   [FR](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-fr.xlsx) ·
   [IT](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-it.xlsx).
   Viene rigenerata automaticamente dopo ogni modifica. **Cominciare sempre con una
   cartella recente.**
2. **Lavorare nelle celle:**

   | Cosa | Come |
   | --- | --- |
   | Modificare un testo | sovrascrivere nella colonna «Testo» (diventa gialla) |
   | Nuovo paragrafo | nella stessa cella, dopo una riga vuota (due volte Alt+Invio, Mac: Ctrl+Opzione+Invio) |
   | Nuova riga / titolo | inserire una **riga intera** (numero di riga → clic destro → Inserisci), scegliere il tipo in «Tipo» (diventa verde) |
   | Eliminare un paragrafo | `!Eliminare!` nella cella (diventa rossa) |
   | Eliminare una pagina intera | `!Eliminare!` nella riga grigia «Pagina» |
   | Cambiare l'ordine | tagliare la riga intera e inserirla nel nuovo punto |

   Inserire o spostare sempre **righe intere**, mai singole celle. Una cella vuota non
   elimina nulla – elimina solo `!Eliminare!`.
3. **Pagina iniziale e team** hanno ciascuno un foglio «… – Vista» (linguetta arancione),
   costruito come il sito. Scrivere solo nelle caselle bianche. Team: compilare una
   scheda vuota = nuova persona, `!Eliminare!` nel nome = persona tolta.
   **Uniguide – Vista** contiene l'intera tabella delle università: una riga per
   università, una colonna per informazione. I testi (intestazioni verdi) valgono per la
   lingua della cartella, il resto per tutte le lingue. I nomi delle colonne si
   sovrascrivono alla riga 4, a destra ci sono colonne vuote per nuove informazioni, la
   riga 5 stabilisce dove compare un'informazione.
   **Domande frequenti – Vista** contiene tutte le domande: compilare una riga vuota in basso = nuova
   domanda, `!Eliminare!` in «Domanda» = domanda tolta (in tutte le lingue).
4. **Nuova stagione:** in alto nel foglio del team compilare «Iniziare una nuova
   stagione» (p. es. 2027/28). Il team attuale passa allora nell'archivio, in tutte e tre
   le lingue.
5. **Caricare:** su GitHub nella cartella [`redaktion/`](../redaktion/) → *Add file →
   Upload files* → *Commit changes*. Dopo uno o due minuti, sotto *Pull requests* compare
   una proposta con un rapporto (cosa è stato ripreso, cosa tralasciato).
   **È online solo quando qualcuno accetta la proposta (Merge).**
   **Come accettare la proposta:** in alto *Pull requests* → cliccare sulla nuova
   proposta → leggere il rapporto. La scheda *Files changed* mostra in rosso ciò che
   sparisce e in verde ciò che si aggiunge. Se è tutto giusto: tornare su
   *Conversation*, in fondo **Merge pull request** → **Confirm merge**. Se nel rapporto
   c'è un ❌ (il sito non si costruisce o la verifica segnala qualcosa), non accettare
   ancora: correggere prima il punto indicato in una cartella recente e caricarla di
   nuovo.

La cartella italiana mostra accanto il testo tedesco come modello; le traduzioni mancanti
sono righe vuote da compilare. Il team in italiano si cura nella cartella italiana.

> **Il repository è pubblico.** Tutto ciò che si trova in una cartella caricata – note
> comprese – resta leggibile per tutti.

Maggiori dettagli (cosa succede esattamente alla lettura, casi di errore): guida
dettagliata, [sezione 3](WARTUNG-DETAILLIERT.it.md#3-cartelle-excel-nel-dettaglio).

---

## 3. Piccole correzioni nell'editor web

**[app.pagescms.org](https://app.pagescms.org)** – accedere con GitHub o tramite l'e-mail di
invito, aprire il repository `Kroeppster/nc-wiki`. A sinistra scegliere la lingua e poi
pagine, notizie o resoconti, modificare il testo come in un programma di videoscrittura e
cliccare **Save**. È subito una modifica su `main`, online uno o due minuti dopo.

Tre regole:

- Lasciare così come sono le caselle grigie `baustein` (team, svolgimento del test,
  generatori …), non scriverci dentro.
- Link alle nostre pagine solo con il percorso, p. es. `/ems/uniguide` (vedi
  [sezione 9](#9-link-e-blocchi-nel-testo)).
- Non rinominare né eliminare pagine nell'editor, ma su GitHub
  ([sezione 8](#8-eliminare-un-file-o-una-pagina)).

La pagina iniziale (linea del tempo, riquadri) e il team si curano meglio con la cartella
Excel.

---

## 4. Scrivere una notizia

**Nell'editor web:** *News* della lingua voluta → creare una nuova voce → compilare
titolo, data, parola chiave (p. es. «Aggiornamento») e testo → **Save**.

**Su GitHub:** in `content/it/news/` creare un nuovo file `mio-titolo.md` (*Add file →
Create new file*). Un modello da copiare si trova in [`docs/vorlage-news.md`](vorlage-news.md)
(in tedesco).

Le prime frasi compaiono automaticamente come anteprima nell'elenco delle notizie e sulla
pagina iniziale. Finché nell'intestazione c'è `draft: true`, l'articolo resta invisibile.
Creare lo stesso articolo anche in tedesco e francese (stesso nome di file sotto
`content/de/news/` e `content/fr/news/`).

Due cose che si dimenticano spesso:

- **Stesso nome di file in tutte le lingue.** L'editor web propone il nome del file a
  partire dal titolo, che cambia da lingua a lingua. Alla creazione inserisci lo stesso
  nome nelle tre lingue (p. es. `testsimulation-2027.md`), altrimenti la scelta della
  lingua in alto a destra non porta all'altra versione.
- **Una data nel futuro** trattiene l'articolo: compare solo quando il giorno è arrivato
  e il sito viene ricostruito dopo.

---

## 5. Caricare un PDF

**Serie di esercizi, simulazione del test, dispensa del corso** – basta caricarli nella
cartella giusta, compaiono automaticamente sul sito:

| Materiale | Cartella |
| --- | --- |
| Serie di esercizi | `assets/downloads/uebungsaufgaben/<subtest>/` (le sottocartelle esistono già) |
| Simulazioni del test | `assets/downloads/testsimulationen/` |
| Dispense dei corsi | `assets/downloads/kursskripte/` |
| Area membri | `assets/downloads/mitglieder/` |

Su GitHub andare nella cartella → *Add file → Upload files* → trascinare il PDF → *Commit
changes*. Le serie si chiamano `<anno>_<nome-cartella>_S<numero>.pdf`, p. es.
`2027_muster-zuordnen_S02.pdf`; la soluzione ha lo stesso nome con `_Loesung` alla fine. Il
nome sul sito ne viene ricavato automaticamente.

**Francese e italiano:** i file di queste lingue vanno nella sottocartella `fr/` o `it/`
della cartella in questione (p. es. `assets/downloads/uebungsaufgaben/muster-zuordnen/it/`),
con lo stesso nome. Ogni versione linguistica del sito mostra solo i file della sua lingua.

**Rapporto annuale e altri documenti singoli** hanno bisogno di una pagina propria – vedi
guida dettagliata, [sezione 2](WARTUNG-DETAILLIERT.it.md#2-pagine-menu-e-navigazione).

---

## 6. Aggiungere un'immagine

Ogni pagina può avere **un'**immagine di copertina (in cima alla pagina e come anteprima
negli elenchi).

1. Caricare l'immagine in `assets/images/<sezione>/`, p. es.
   `assets/images/news/simulazione-2027.jpg`.
2. Aggiungere nell'intestazione della pagina:

   ```yaml
   featured_image: "news/simulazione-2027.jpg"
   featured_image_alt: "Breve descrizione di cosa mostra l'immagine"
   ```

   Il percorso comincia **dopo** `assets/images/`. La descrizione è obbligatoria (per chi
   usa un lettore di schermo); senza, la costruzione fallisce.

Le immagini grandi non sono un problema – il sito le rimpicciolisce da solo.

**Immagini nel testo** (p. es. schermate in una notizia): caricare anche queste in
`assets/images/<sezione>/` e inserirle nel testo su una riga a sé:

```markdown
![Cosa mostra l'immagine](news/neue-website/it/uniguide.png "Didascalia")
```

La descrizione tra parentesi quadre è obbligatoria, la didascalia tra virgolette
facoltativa. Anche qui il percorso comincia **dopo** `assets/images/`. Se è sbagliato, la
costruzione fallisce con un messaggio.

---

## 7. Creare una nuova pagina

1. Su GitHub andare nella cartella voluta sotto `content/it/` → *Add file → Create new
   file*.
2. Nome del file: minuscolo, senza accenti né spazi, termina con `.md`
   (p. es. `nuova-pagina.md`). Fa parte dell'indirizzo – deve essere **identico** nelle
   tre lingue.
3. Contenuto:

   ```markdown
   ---
   title: "Titolo della pagina"
   description: "Una frase che compare in Google sotto il titolo (max. 160 caratteri)."
   ---

   Testo della pagina.
   ```

4. Creare lo stesso file, tradotto, sotto `content/de/` e `content/fr/`.

Perché la pagina compaia nel menu: guida dettagliata,
[sezione 2](WARTUNG-DETAILLIERT.it.md#2-pagine-menu-e-navigazione).

---

## 8. Eliminare un file o una pagina

Aprire il file su GitHub → in alto a destra **…** → *Delete file* → *Commit changes*.

- Eliminare una pagina in **tutte e tre le lingue**.
- Per le serie di esercizi eliminare l'esercizio **e** il file `_Loesung`.
- Se un link punta ancora alla pagina eliminata, la costruzione diventa rossa e indica il
  punto – togliere lì il link.

---

## 9. Link e blocchi nel testo

**Link interni:** un link normale con il percorso, senza la lingua:

```markdown
Maggiori informazioni nell'[Uniguide](/ems/uniguide).
```

Sulla pagina italiana diventa automaticamente il link alla pagina italiana. Se la pagina
di destinazione non esiste, la costruzione si interrompe con un messaggio – così nessun
link morto va online.

**Blocchi** (schede del team, tabella dello svolgimento, generatori, contatto
sponsorizzazione): una casella grigia nel testo:

````markdown
```baustein
team-leitung
```
````

Si possono spostare, ma non scriverci dentro. Non scrivere mai `{{< … >}}` nel testo –
l'editor web le distrugge.

---

## 10. Quando la costruzione è rossa

**Il sito resta online** – manca solo l'ultima modifica finché l'errore non è corretto.

1. Su GitHub in alto **Actions** → aprire l'ultima esecuzione con ✗ rossa → job **build**.
2. Aprire il passaggio con ✗; di solito vi è indicato il file interessato.

| Rosso a | Di solito | Cosa fare |
| --- | --- | --- |
| «Check internal links», o «Build with Hugo» con «Link» | un link punta nel vuoto | correggere il link nel file indicato |
| «Check built site» | una pagina senza titolo, descrizione o titolo principale, un indirizzo senza `/nc-wiki/` o un testo dell'area membri visibile senza protezione | il messaggio indica il tipo e il file; correggere nel file indicato |
| «Build with Hugo» | errore nell'intestazione (virgolette, rientro, descrizione immagine mancante) | confrontare con un file che funziona |

I link verso altri siti sono controllati una volta alla settimana da un'esecuzione a
parte («Externe Links prüfen»); se è rossa, uno di questi link è rotto, il sito stesso
funziona normalmente. Lo stesso vale per «Prüfstand» (ogni notte): percorre il sito in
un browser e non lo modifica. Se non sai andare avanti: sotto
*Issues → New issue* pubblicare il link all'esecuzione rossa.

Per una pull request lo stesso controllo gira già prima dell'accettazione – una ✗ rossa
significa: non unire ancora.

---

## 11. Modificare un file direttamente su GitHub

Per tutto ciò che l'editor web non offre, o se preferisci lavorare su GitHub.

1. Aprire [github.com/Kroeppster/nc-wiki](https://github.com/Kroeppster/nc-wiki) e
   accedere.
2. **Trovare il file.** Le pagine stanno sotto `content/it/` (tedesco: `content/de/`,
   francese: `content/fr/`), organizzate come gli indirizzi del sito:

   | Indirizzo della pagina | File |
   | --- | --- |
   | `…/nc-wiki/it/impressum/` | `content/it/impressum.md` |
   | `…/nc-wiki/it/ems/` | `content/it/ems/_index.md` (pagina d'insieme di una cartella) |
   | `…/nc-wiki/ems/uniguide/` | `content/de/ems/uniguide/_index.md` |

   Più veloce: digitare una parte del nome nel campo *Go to file*, in alto.
3. Cliccare sul file → in alto a destra l'**icona della matita** (*Edit this file*).
4. Modificare il testo. Nell'intestazione (tra i `---`) cambiare solo ciò che sta tra
   virgolette; le parole prima dei due punti e il rientro restano.
5. In alto a destra **Commit changes…** → descrivere in una frase che cosa hai cambiato →
   **Commit changes**.
6. Aspettare uno o due minuti e ricaricare la pagina
   ([sezione 12](#12-controllare-e-annullare)).

---

## 12. Controllare e annullare

**La mia modifica è online?** Su GitHub, in alto, **Actions**. L'esecuzione più recente
«Deploy Hugo site to GitHub Pages» mostra lo stato:

| Segno | Significato |
| --- | --- |
| cerchio giallo | la costruzione è in corso (circa due minuti) |
| spunta verde | finito, la modifica è online |
| croce rossa | un errore, la modifica **non** è online ([sezione 10](#10-quando-la-costruzione-è-rossa)) |

Poi ricaricare la pagina nel browser, meglio senza la cache: Ctrl+F5 (Windows) o
Cmd+Shift+R (Mac).

**La modifica non compare?** Controllare nell'ordine:

1. La costruzione è verde? (vedi sopra)
2. Cartella Excel caricata: la proposta sotto *Pull requests* è già stata accettata?
3. Nell'intestazione c'è `draft: true`, o la data è nel futuro? Allora la pagina resta
   nascosta.
4. Stai guardando la lingua giusta? Una modifica sotto `content/it/` si vede solo sulla
   pagina italiana.
5. Il file è nella cartella giusta e finisce con `.md`?

**Annullare qualcosa**

- **Una cartella Excel accettata (pull request):** *Pull requests* → *Closed* → aprire la
  proposta → in fondo **Revert** → nasce una nuova proposta che annulla tutto →
  accettarla (Merge).
- **Un singolo file:** aprire il file → in alto a destra **History**. Lì c'è ogni versione
  con data e descrizione. Cliccare sulla versione che era ancora giusta → in alto a
  destra **…** → *View file* → copiare il testo. Tornare al file attuale, icona della
  matita, sostituire tutto con il testo copiato, **Commit changes**.
- **Un file eliminato, o se non sei sicuro·a:** descrivere che cosa è successo sotto
  *Issues → New issue*. Non si perde nulla; qualcuno con più esperienza lo recupera.

---

## 13. Lista di controllo per il nuovo anno

Una volta all'anno, appena è nota la data del prossimo AMS.

| Che cosa | Dove | Come |
| --- | --- | --- |
| data del prossimo AMS (conto alla rovescia sulla pagina iniziale) | file `hugo.toml`, riga `ems_exam_date` | come nella [sezione 11](#11-modificare-un-file-direttamente-su-github): cambiare solo la data tra le virgolette. Forma: `2027-07-09T08:00:00+02:00` significa 9 luglio 2027, ore 8, ora legale svizzera. Il testo sopra il conto alla rovescia riprende la data da solo |
| date nella linea del tempo della pagina iniziale | cartella Excel, foglio della pagina iniziale (vista) | [sezione 2](#2-modificare-i-testi-con-la-cartella-excel) |
| data nelle domande frequenti | cartella Excel, foglio delle domande frequenti (vista) | sezione 2 |
| data sulla pagina «AMS» | editor web, pagina «AMS» | [sezione 3](#3-piccole-correzioni-nelleditor-web) |
| termini e «stato» nell'Uniguide | cartella Excel, foglio dell'Uniguide (vista) | sezione 2; inserire solo ciò che figura su una pagina ufficiale |
| nuova stagione del team | cartella Excel, foglio del team (vista), «Iniziare una nuova stagione» | sezione 2 |
| nuova simulazione del test, nuove serie di esercizi | caricare i PDF | [sezione 5](#5-caricare-un-pdf) |
| soluzioni per «valutare il foglio delle risposte» e «valutare il test di concentrazione» | serve qualcuno con conoscenze tecniche | [guida dettagliata, sezione 11](WARTUNG-DETAILLIERT.it.md) |

Alla fine cercare l'anno vecchio sul sito con la lente: ciò che compare ancora e non è
una retrospettiva è stato dimenticato.

---

## 14. Aiuto per scrivere

Così si scrive in un file `.md` e nella colonna «Testo» della cartella Excel. Nell'editor
web ci sono i pulsanti per questo.

| Vuoi | Scrivi |
| --- | --- |
| un titoletto | `## Titolo` (più piccolo: `### Titolo`). Mai un solo `#`, il titolo della pagina è già il titolo principale |
| il grassetto | `**importante**` |
| un elenco puntato | ogni riga inizia con `- ` |
| un elenco numerato | ogni riga inizia con `1. `, `2. ` … |
| un nuovo paragrafo | una riga vuota in mezzo |
| un link a una pagina del sito | `[Uniguide](/ems/uniguide)` ([sezione 9](#9-link-e-blocchi-nel-testo)) |
| un link a un altro sito | `[swissuniversities](https://www.swissuniversities.ch/)` |
| un asterisco visibile (p. es. l'asterisco di genere in un testo tedesco) | `Tutor\*innen`, con una barra rovesciata davanti all'asterisco. Senza, Markdown mette in corsivo ciò che sta tra due asterischi dello stesso paragrafo, e la costruzione si ferma con un messaggio. Nell'editor web digitare semplicemente `*` |
| le virgolette | «così», non "così" |

Come scriviamo (dare del tu, termini, data «9 luglio 2027») è descritto nella
[guida di stile](STYLEGUIDE.md) (in tedesco).

---

## 15. Le regole più importanti

- **Tutto in tre lingue.** I nuovi testi visibili sempre in tedesco, francese e italiano.
- **Stesso nome di file in tutte le lingue.** Solo così la scelta della lingua trova le
  altre versioni di una pagina.
- **Il repository è pubblico.** Niente password, dati personali o note interne nei file o
  nelle cartelle Excel. Gli accessi vanno nel gestore di password dell'associazione.
- **Non inventare numeri.** Nell'Uniguide inserire solo ciò che figura su una pagina
  ufficiale; i numeri della pagina iniziale li conta il sito stesso.
- **L'indicazione di licenza resta.** Gli esercizi sono sotto licenza CC BY-NC 4.0;
  l'indicazione non si toglie.
- **Nel dubbio chiedere** prima di modificare qualcosa in `layouts/`, `.github/` o
  `hugo.toml`.
