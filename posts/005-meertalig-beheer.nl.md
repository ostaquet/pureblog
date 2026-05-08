---
title: Meertalig beheer
date: 2026-05-02
excerpt: Meertalige integratie is een sterk punt van Pureblog. Ontdek hoe Pureblog anders is en hoe talen worden beheerd om de beste gebruikerservaring en de beste SEO te garanderen.
---

Pureblog is in de eerste plaats een meertalige blogengine. Het is gemaakt na talloze pogingen met bestaande oplossingen (WordPress, Ghost, Bearblog, Drupal, Chirpy/Jekyll). Bij elke poging voelde de meertalige afhandeling meer aan als geknutsel dan als iets dat geïntegreerd was in de engine. Geknutsel werkt visueel voor de bezoeker, maar heeft een negatieve impact op SEO en gebruikerservaring bij gebruik met een RSS-feed.

## Startpagina's en indexen

De startpagina's van de verschillende talen worden onderscheiden door een URL-uitbreiding. Hierdoor kan per taal een RSS-feed behouden blijven, zodat de bezoeker de berichten van je Pureblog in zijn voorkeurstaal kan lezen.

De Pureblog die je nu leest, is bijvoorbeeld in meerdere talen beschikbaar. Er zijn dus meerdere URLs om de indexen te bereiken:

- <https://www.pureblog.dev/en>
- <https://www.pureblog.dev/fr>
- <https://www.pureblog.dev/nl>
- ...

De beschikbare talen worden gedefinieerd in het configuratiebestand `config/config.yml` onder de parameter `languages.codes`. De eerste opgegeven taal is altijd de standaardtaal.

De standaardtaal wordt gebruikt voor de doorverwijzing vanaf de basis-URL van je Pureblog. Voor deze Pureblog is de standaardtaal `en` (Engels). Een bezoeker die de URL <https://www.pureblog.dev> opent, wordt dus automatisch doorgestuurd naar <https://www.pureblog.dev/en>.

Elke pagina van je Pureblog bevat een taalwisselaar (_language switcher_), inclusief de startpagina's. Met deze wisselaar kan de bezoeker snel naar de gewenste taal overschakelen.

## RSS-feeds en de sitemap

Elke taal heeft zijn eigen RSS-feed. Hiermee kunnen bezoekers de berichten van je Pureblog in hun voorkeurstaal volgen. RSS-feeds zijn altijd gekoppeld onder een taal-URL, in de vorm <https://www.pureblog.dev/nl/feed.xml>.

De sitemap is uniek voor de gehele site. Hij bevat de startpagina's en de berichten. Voor elke pagina vermeldt de sitemap de taal en de beschikbare alternatieve talen voor die pagina, evenals de URLs. Dit is vaak het punt waar andere blogengines tekortschieten, omdat ze geen alternatieve links tussen berichten in de sitemap beheren.

Voor meer over RSS-feeds en sitemaps, zie [de pagina over online zichtbaarheid](posts/006-online-zichtbaarheid.nl.md).

## Links tussen talen voor hetzelfde bericht

Om de SEO te verbeteren kan een bericht een andere URL hebben afhankelijk van de taal. Dit is ook een verschil ten opzichte van traditionele blogengines.

De URL wordt altijd opgebouwd uit de bestandsnaam van het bericht. De bestandsnaam heeft de vorm `<id>-<slug>.<lang>.md`. De `id`-identificatie verbindt dezelfde pagina geschreven in verschillende talen. De `slug` is de URL die zal worden gebruikt. De taal is de ISO-code van 2 tekens (`lang`). Een bestand met de naam `002-schrijf-nieuw-bericht.nl.md` zal dus worden aangeboden onder de URL `/nl/schrijf-nieuw-bericht/`.

Een bericht dat in meerdere talen is geschreven, kan per taal verschillende URLs hebben. Bijvoorbeeld:

- `002-write-new-post.en.md` voor het Engels.
- `002-ecrire-nouvel-article.fr.md` voor het Frans.
- `002-schrijf-nieuw-bericht.nl.md` voor het Nederlands.
- ...

De identificatie fungeert als verbindingselement tussen de verschillende talen van hetzelfde bericht (in het voorbeeld is de identificatie `002`).

Zoals hierboven vermeld, bevat elke pagina van je Pureblog een taalwisselaar. Deze wisselaar is duidelijk zichtbaar zodat de bezoeker het bericht in een andere taal kan lezen. Als het bericht niet beschikbaar is in een taal, geeft de wisselaar de doorgestreepte taalcode weer (bv. ~~NL~~ ). Klikt de bezoeker toch op de doorgestreepte link, dan wordt hij naar de huidige pagina teruggeleid.

Wanneer een bericht in één taal bestaat maar niet in de andere, wordt tijdens de generatie van de site een waarschuwing weergegeven.

## Taalconfiguratie

De beschikbare talen zijn opgegeven in het configuratiebestand `config/config.yml` in de sectie `languages`. Deze sectie bevat een reeks parameters waarmee je de taalconfiguratie kunt fijn afstellen.

```
languages:
  codes:
    - en
    - fr
    - nl
  reading_time_labels:
    en: "min read"
    fr: "min de lecture"
    nl: "min leestijd"
  back_labels:
    en: "← Back"
    fr: "← Retour"
    nl: "← Terug"
```

De taalcodes worden vermeld onder de parameter `languages.codes`. De taalcodes zijn opgegeven in [ISO 639-1](https://nl.wikipedia.org/wiki/Lijst_van_ISO_639-1-codes) (taalcodes van 2 letters).

De eerste taalcode is de standaardtaal van je Pureblog.

De parameters `languages.reading_time_labels` en `languages.back_labels` zijn de labels die tijdens het genereren van de site worden gebruikt om het aantal leesminuten van een bericht en het terug-naar-startpagina-label aan te geven.

## Wat gebeurt er als een bericht slechts in één taal bestaat?

De startpagina's, de sitemap en de RSS-feeds steunen uitsluitend op de aanwezigheid van berichtbestanden. Als een bestand niet bestaat (bv. de NL-versie), verschijnt het bericht dus nergens op je Pureblog.

Als het bericht niet beschikbaar is in een taal, toont de taalwisselaar de doorgestreepte taalcode (bv. ~~NL~~ ). Klikt de bezoeker toch op de doorgestreepte link, dan wordt hij naar de huidige pagina teruggeleid.

Wanneer een bericht in één taal bestaat maar niet in de andere, wordt tijdens de generatie van de site een waarschuwing weergegeven.

## Werkt Pureblog met één enkele taal?

Ja, Pureblog kan met één enkele taal worden gebruikt. In dat geval volstaat het om één taalcode op te geven in het configuratiebestand (`languages.codes`).

Merk op dat het doorverwijzingsgedrag identiek blijft. Als je enkel de taalcode `en` gebruikt, wordt de startpagina `https://www.example.com` toch doorgestuurd naar `https://www.example.com/en`. Hierdoor kunnen later talen worden toegevoegd en kun je starten met een eentalige Pureblog.

Wanneer slechts één taal is geconfigureerd, wordt de taalwisselaar niet weergegeven op de startpagina's en de berichtpagina's. In de minimalistische geest is het zinloos de pagina te vervuilen met een wisselaar die zijn nut heeft verloren.
