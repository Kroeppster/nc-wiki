# Curare il sito – guida breve

[Deutsch](WARTUNG.md) · [Français](WARTUNG.fr.md) · **Italiano**

Qui c'è solo il lavoro di tutti i giorni: modificare testi, scrivere una notizia, caricare
PDF e immagini, eliminare qualcosa. Tutto si fa nel browser, non serve installare nulla.
Tutto il resto (pagina iniziale, team, menu, design, moduli, area membri, tecnica) si
trova nella **[guida dettagliata](WARTUNG-DETAILLIERT.it.md)**.

I nomi di file e cartelle (`content/de/…`, `redaktion/` …) restano in tedesco, perché sono
i nomi reali nel repository.

---

## 1. Quale strumento per cosa

| Vuoi … | Strumento | Sezione |
| --- | --- | --- |
| rileggere molti testi, tradurre, modificare la pagina iniziale o il team | **cartella Excel** | [2](#2-modificare-i-testi-con-la-cartella-excel) |
| correggere in fretta un errore su una pagina | **editor web** (Pages CMS) | [3](#3-piccole-correzioni-nelleditor-web) |
| scrivere una notizia | editor web o GitHub | [4](#4-scrivere-una-notizia) |
| caricare un PDF o un'immagine, eliminare un file | **GitHub** | [5](#5-caricare-un-pdf) – [8](#8-eliminare-un-file-o-una-pagina) |

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
| «Build with Hugo» | errore nell'intestazione (virgolette, rientro, descrizione immagine mancante) | confrontare con un file che funziona |

«Check external links» è solo un avviso e non rompe nulla. Se non sai andare avanti: sotto
*Issues → New issue* pubblicare il link all'esecuzione rossa.

Per una pull request lo stesso controllo gira già prima dell'accettazione – una ✗ rossa
significa: non unire ancora.

---

## 11. Le regole più importanti

- **Tutto in tre lingue.** I nuovi testi visibili sempre in tedesco, francese e italiano.
- **Il repository è pubblico.** Niente password, dati personali o note interne nei file o
  nelle cartelle Excel. Gli accessi vanno nel gestore di password dell'associazione.
- **Non inventare numeri.** Nell'Uniguide inserire solo ciò che figura su una pagina
  ufficiale; i numeri della pagina iniziale li conta il sito stesso.
- **L'indicazione di licenza resta.** Gli esercizi sono sotto licenza CC BY-NC 4.0;
  l'indicazione non si toglie.
- **Nel dubbio chiedere** prima di modificare qualcosa in `layouts/`, `.github/` o
  `hugo.toml`.
