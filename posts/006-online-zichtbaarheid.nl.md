---
title: Online zichtbaarheid
date: 2026-05-01
excerpt: Pureblog bevat van bij de start een reeks mechanismen om de zichtbaarheid van je Pureblog op zoekmachines en in LLM's te verbeteren. Ontdek de ingebouwde oplossingen zoals SEO-tags (Search Engine Optimization), sitemaps en RSS-feeds.
---

De zichtbaarheid van je inhoud online is een belangrijk punt om niet uit het oog te verliezen als je een publiek wilt opbouwen of meer bescheiden je gedachten wilt delen. Pureblog is van meet af aan ontworpen om de beste indexering van je inhoud op zoekmachines (Google, Bing, enz.) en op LLM's (ChatGPT, Claude, Gemini, enz.) mogelijk te maken.

Deze pagina legt de in Pureblog ingebouwde functies uit die de zichtbaarheid van je inhoud verbeteren.

## Core Web Vitals (_back to the basics_)

Core Web Vitals zijn metrieken van Google die de echte gebruikerservaring van een website beoordelen via laadsnelheid (_LCP_), reactievermogen (_INP_) en visuele stabiliteit (_CLS_). Ze zijn essentieel voor SEO (_Search Engine Optimization_, of rangschikkingsfactoren); ze richten zich op specifieke drempelwaarden, namelijk een _LCP_ ≤ 2,5 s, een _INP_ ≤ 200 ms en een _CLS_ ≤ 0,1, geanalyseerd in de [Google Search Console](https://search.google.com/search-console).

De 3 Core Web Vitals zijn:

- **Laadsnelheid** of [LCP (Largest Contentful Paint)](https://web.dev/articles/lcp): Dit meet de tijd die nodig is om het grootste zichtbare element (afbeelding, tekstblok) op het scherm weer te geven. Een goede LCP is kleiner of gelijk aan 2,5 seconden.
- **Reactievermogen bij interactie** of [INP (Interaction to Next Paint)](https://web.dev/articles/inp): Dit meet de latentie van alle gebruikersinteracties (klikken, tikken). De meting is gebaseerd op de slechtste interactie. Het vervangt _FID (First Input Delay)_ sinds maart 2024, met een streefwaarde van 200 milliseconden of minder.
- **Visuele stabiliteit** of [CLS (Cumulative Layout Shift)](https://web.dev/articles/cls): Dit meet onverwachte lay-outverschuivingen. De score moet kleiner of gelijk aan 0,1 zijn om stabiele navigatie te garanderen.

Deze elementen worden in Pureblog op twee manieren behandeld:

1. Je volledige Pureblog is statische HTML. Dat wil zeggen dat het tijdens de generatie wordt gebouwd. De pagina's zijn licht en vereisen geen nabewerking in de browser van de bezoeker. Dit betekent dat _LCP_ en _INP_ extreem laag blijven, zelfs met veel inhoud.
2. Alle pagina's hebben één formaat gebaseerd op een template waarover je de controle hebt. Het template zorgt voor consistentie binnen je Pureblog en blijft tegelijk aanpasbaar (zie ook [hoe je het ontwerp van je Pureblog aanpast](posts/004-ontwerp-opmaak-en-typografie.nl.md)).

**TODO VOEG EEN SCREENSHOT TOE VAN DE CORE VITALS VAN DEZE SITE NA PUBLICATIE**

## Belangrijke SEO-elementen

Alle belangrijke SEO-elementen worden door Pureblog beheerd.

Wanneer je een Google-zoekresultaat aandachtig bekijkt, vind je de volgende sleutelelementen:

- De sitetitel
- Het pictogram (_favicon_)
- De URL
- De paginatitel
- De paginabeschrijving

![Anatomie van een Google-zoekresultaat](assets/img/anatomie_google_entry_nl.png)

De sitetitel wordt gedefinieerd in het configuratiebestand (`config/config.yml`) met de parameter `general.site_title`.

Het sitepictogram (favicon) wordt automatisch door Pureblog gegenereerd uit een enkele emoji die is gedefinieerd in de parameter `theme.favicon_emoji` van het configuratiebestand (bv. `📝`). Pureblog produceert een SVG-bestand dat beschikbaar is op `/favicon.svg` en verwijst ernaar op elke pagina van de site, zonder dat externe grafische bronnen nodig zijn.

De URL wordt bepaald door de `slug` van de pagina en de taalcode. De `slug` is afgeleid van de naam van het Markdown-bestand. De `slug` is belangrijk voor SEO.

De paginatitel en -beschrijving worden gedefinieerd in de front matter van het bericht via respectievelijk de tags `title` en `excerpt`.

Elk blogbericht heeft een beschrijving (`excerpt` in de front matter van je bericht). Deze beschrijving wordt automatisch gegenereerd op basis van de eerste 200 tekens van je bericht als ze niet is gedefinieerd. De beschrijving wordt gebruikt in de meta-tag van je berichtpagina's (`<meta name="description" content="..."/>`).

## Het onderscheid tussen titel en URL

Veel blogs gebruiken de paginatitel als URL. Wij vinden dat een slecht idee. De paginatitel kan immers "leeg-woorden" bevatten (zoals "de", "een", enz.). De URL heeft die "leeg-woorden" niet nodig. De URL moet zo kort mogelijk zijn en sleutelwoorden bevatten die nuttig zijn voor SEO. Bovendien zou een wijziging in de paginatitel om een typfout te corrigeren geen reeds elders of in zoekmachines geïndexeerde URLs mogen breken.

Daarom zijn de paginatitel en de URL twee onderscheiden begrippen in Pureblog.

De paginatitel (die op de pagina verschijnt en zichtbaar is voor bezoekers) wordt gedefinieerd in de front matter van het bericht (onder de tag `title`). Het is ook deze titel die wordt gebruikt om de indexen op te bouwen die alle pagina's van de site oplijsten.

De URL daarentegen wordt opgebouwd uit de bestandsnaam van het bericht. De bestandsnaam heeft de vorm `<id>-<slug>.<lang>.md`. De `id`-identificatie verbindt dezelfde pagina geschreven in verschillende talen. De `slug` is de URL die zal worden gebruikt. De taal is de ISO-code van 2 tekens (`lang`).

Een bestand met de naam `002-schrijf-nieuw-bericht.nl.md` zal dus worden aangeboden onder de URL `/nl/schrijf-nieuw-bericht/`.

## De sitemap

Een sitemap is een XML-bestand dat de essentiële pagina's, video's en bestanden van een website oplijst voor zoekmachines. Hij fungeert als een kaart en helpt crawlers om inhoud efficiënt te ontdekken en te indexeren, vooral voor nieuwe sites of complexe structuren.

Voor een blog helpt hij ook om ervoor te zorgen dat alle pagina's zijn geïndexeerd, ook degene die niet meer op de hoofdpagina van de site staan (bv. op een 2e of 3e pagina).

Waarom is de sitemap belangrijk?

- **Snelle en volledige indexering**: hij stelt Google en andere zoekmachines in staat snel alle pagina's te vinden, zelfs slecht onderling verbonden pagina's (zwakke interne linking).
- **Gemelde updates**: hij geeft crawlers de laatste wijzigingsdatum van de pagina's door, waardoor ze worden aangemoedigd terug te keren en de index te vernieuwen.
- **SEO-optimalisatie**: hij helpt de structuur van de site beter over te brengen en specifieke inhoud (video's, afbeeldingen, nieuws) te indexeren.
- **Vereist voor sommige sites**: cruciaal voor grote sites, recente sites met weinig externe links, of sites die veel rijke inhoud (video) gebruiken.

Pureblog genereert automatisch een sitemap-bestand voor je volledige Pureblog, rekening houdend met vertalingen en de beschikbaarheid van talen. Voor elke pagina wordt de laatste wijzigingsdatum (`<lastmod>`) afgeleid van de berichtdatum; voor indexpagina's wordt de datum gebruikt van het meest recente bericht in de betrokken taal.

Het sitemap-bestand is beschikbaar op de URL <https://www.example.com/sitemap.xml> en wordt automatisch gerefereerd in de `robots.txt` om de ontdekking ervan door crawlers (zoekmachines en LLM's) te vergemakkelijken.

Voorbeeld van een sitemap voor deze Pureblog: <https://www.pureblog.dev/sitemap.xml>.

## RSS-feeds

De RSS-feed (_Really Simple Syndication_) is een XML-bestandsformaat waarmee frequent bijgewerkte webcontent (artikels, nieuws, podcasts) kan worden gesyndiceerd en automatisch verspreid. Hiermee kunnen gebruikers zich abonneren op hun favoriete sites en nieuwe updates ontvangen zonder elke site afzonderlijk te moeten bezoeken.

Gebruikers kunnen de laatste publicaties als samenvattingen of integrale teksten raadplegen via speciale lezers zoals [Feedly](https://feedly.com/), [Inoreader](https://www.inoreader.com/) of browserextensies.

Pureblog levert per taal een RSS-feed. RSS-feeds worden automatisch gegenereerd tijdens het bouwen van je Pureblog. RSS-feeds zijn beschikbaar via URLs in de vorm `https://www.example.com/<lang>/feed.xml`.

Voor de taal die je nu op deze site leest, is de RSS-feed beschikbaar op <https://www.pureblog.dev/nl/feed.xml> en wordt op elke pagina gerefereerd in een `<link>`-tag voor automatische ontdekking (_RSS autodiscovery_) zodat externe applicaties hem gemakkelijk kunnen vinden.

Een RSS-feed bestaat altijd uit een verzameling artikelen.

Elk artikel bevat:

- Een titel die in de front matter van je bericht is gedefinieerd (tag `title`)
- Een beschrijving die in de front matter van je bericht is gedefinieerd (tag `excerpt`). Als deze tag niet is gedefinieerd, gebruikt Pureblog automatisch de eerste 200 tekens van je bericht.
- Het publicatiemoment dat is samengesteld uit de datum in de front matter van je bericht (tag `date`) en de configuratie (`publish.default_timezone` en `publish.default_publish_hour`).
- Een permalink op basis van de bestandsnaam van je bericht (de bekende `slug`). ⚠️ Het is belangrijk om deze _slugs_ niet te veel te wijzigen, anders heeft het een negatieve impact op de rangschikking in zoekmachines.

## Configuratiebestanden voor zoekmachines en LLM's

Pureblog beheert ook een aanvullend configuratiebestand voor zoekmachines en LLM's.

Het bestand `robots.txt` is een tekstbestand dat in de hoofdmap van een website wordt geplaatst en instructies geeft aan crawlers over welke pagina's ze moeten verkennen of niet. Het wordt vooral gebruikt om het crawlbudget te beheren en de toegang tot privégebieden te blokkeren, maar het verhindert geen indexering als de pagina elders wordt gelinkt.

Pureblog steunt op het bestand `robots.txt` waarnaar wordt verwezen in de configuratie (`config/config.yml`) onder de parameter `seo.robots_file`. Tijdens de build wordt het opgegeven bestand naar de uiteindelijke site gekopieerd en wordt de directieve `Sitemap:` automatisch toegevoegd op het einde (enkel als ze er nog niet staat). Je kunt de inhoud van je bron-`robots.txt` dus vrij beheren zonder vrees voor duplicatie.

Het bestand `robots.txt` is beschikbaar op de URL <https://www.pureblog.dev/robots.txt>.

## Aangepaste 404-pagina

Wanneer een bezoeker op een niet-bestaand URL van je site terechtkomt, ziet hij een 404-fout. Standaard toont de host een kale, niet-opgemaakte foutpagina. Pureblog genereert automatisch een gestijlde `404.html` in de rootmap van de site die de visuele identiteit van je blog weerspiegelt. De bezoeker blijft zo in een consistente omgeving en kan gemakkelijk de weg terug naar de startpagina vinden.

De pagina is volledig zelfstandig: de stylesheet is rechtstreeks in de HTML ingebed en alle links gebruiken de absolute URL die is geconfigureerd in `general.site_url`. Dit garandeert dat stijlen en navigatie correct werken, ongeacht de URL-diepte waarop de host de foutpagina serveert (Firebase serveert bijvoorbeeld dezelfde `404.html` of de ontbrekende URL nu `/brol` of `/en/brol` is).

De pagina toont het bericht "pagina niet gevonden" in de standaardtaal en een link naar de startpagina. Beide teksten worden geconfigureerd in `config/config.yml` onder de sectie `languages`:

```yaml
languages:
  not_found_labels:
    en: "Page not found"
    fr: "Page introuvable"
    nl: "Pagina niet gevonden"
  not_found_home_labels:
    en: "← Go to homepage"
    fr: "← Aller à l'accueil"
    nl: "← Naar de startpagina"
```

Er is ook een taalkiezer opgenomen met directe links naar de index van elke geconfigureerde taal, zodat bezoekers kunnen navigeren, zelfs na het landen op een ontbrekende URL.

Op Firebase Hosting wordt het bestand `404.html` in de root automatisch geserveerd voor elke niet-overeenkomende URL. Andere statische hosters (Netlify, GitHub Pages, enz.) volgen dezelfde conventie.

## Andere nuttige functies

Pureblog is compatibel met de leesmodi van webbrowsers zonder dat de lay-out wordt aangetast.
