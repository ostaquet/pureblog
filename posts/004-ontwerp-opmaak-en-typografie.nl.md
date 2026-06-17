---
title: Ontwerp, opmaak en typografie
date: 2026-05-03
excerpt: Enkele voorbeelden van typografie, afbeeldingen en links; evenals de belangrijkste bestanden om het ontwerp aan jouw smaak aan te passen.
---

Pureblog is gebouwd rond een minimalistisch ontwerp dat voldoet aan de behoeften voor het publiceren van blogposts.

# Typografische voorbeelden

## Koppen en sectietitels

```
# Kop niveau 1
## Kop niveau 2
### Kop niveau 3
#### Kop niveau 4
```

# Kop niveau 1

## Kop niveau 2

### Kop niveau 3

#### Kop niveau 4

## Paragrafen en opmaak

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar urna erat, et sollicitudin mi sodales id. Quisque sit amet egestas ex. Proin id diam ante. Duis varius porttitor luctus. Maecenas tempus nunc sed enim vehicula, sit amet laoreet turpis eleifend. Nunc vel sollicitudin neque. Quisque at laoreet metus. Proin sed odio nec urna eleifend interdum. Integer luctus magna nec neque consequat sagittis.
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar urna erat, et sollicitudin mi sodales id. Quisque sit amet egestas ex. Proin id diam ante. Duis varius porttitor luctus. Maecenas tempus nunc sed enim vehicula, sit amet laoreet turpis eleifend. Nunc vel sollicitudin neque. Quisque at laoreet metus. Proin sed odio nec urna eleifend interdum. Integer luctus magna nec neque consequat sagittis.

```
**Vetgedrukte tekst**
_Cursieve tekst_
*Cursieve tekst*
~~Doorgestreepte tekst~~
`Inline code`
> Citaat
```

**Vetgedrukte tekst**

_Cursieve tekst_

_Cursieve tekst_

~~Doorgestreepte tekst~~

`Inline code`

> Citaat

Lege regels scheiden paragrafen. Een eenvoudige regelafbreking binnen een paragraaf wordt geconverteerd naar een spatie, conform het standaardgedrag van Markdown.

Opmerking: doorhalen (`~~…~~`) wordt opzettelijk genegeerd binnen inline code (tussen enkele backticks) en codeblokken (tussen drievoudige backticks), zodat codevoorbeelden ongewijzigd worden weergegeven.

## Opsommingen

```
- Eerste item
- Tweede item
- Derde item
```

- Eerste item
- Tweede item
- Derde item

## Genummerde lijsten

```
1. Eerste item
2. Tweede item
3. Derde item
```

1. Eerste item
2. Tweede item
3. Derde item

## Code

Inline code in tekst:

```
`Inline code`
```

`Inline code`

Meerdere regels code:

````
```
def hello() -> str:
    return "world"
```
````

```
def hello() -> str:
    return "world"
```

Er is geen automatische regelafbreking bij het opmaken van meerdere regels code.

# Linkvoorbeelden

Er zijn 4 soorten links:

- Automatische links (`<http://www.example.com>`)
- Externe links in hetzelfde tabblad (`[Open in hetzelfde tabblad](http://www.example.com)`)
- Externe links in een nieuw tabblad (`[Open in een nieuw tabblad](tab:http://www.example.com)`)
- Interne links in hetzelfde tabblad (`[Interne link](posts/001-eerste-stappen.nl.md)`)

Het voorvoegsel `tab:` en interne links kunnen worden gecombineerd. Bijvoorbeeld, `[Interne link in een nieuw tabblad](tab:posts/001-eerste-stappen.nl.md)` opent de opgeloste interne link in een nieuw tabblad.

🔐 Beveiligingsopmerking: links die in een nieuw tabblad worden geopend (`tab:`) krijgen automatisch de attributen `target="_blank"` en `rel="noopener noreferrer"`, wat je bezoekers beschermt tegen _tabnabbing_.

```
<http://www.example.com>
[Open in hetzelfde tabblad](http://www.example.com)
[Open in een nieuw tabblad](tab:http://www.example.com)
[Interne link](posts/001-eerste-stappen.nl.md)
[Interne link in een nieuw tabblad](tab:posts/001-eerste-stappen.nl.md)
```

<http://www.example.com>

[Open in hetzelfde tabblad](http://www.example.com)

[Open in een nieuw tabblad](tab:http://www.example.com)

[Interne link](posts/001-eerste-stappen.nl.md)

[Interne link in een nieuw tabblad](tab:posts/001-eerste-stappen.nl.md)

Als een interne link in tekst wordt gebruikt maar niet bestaat, wordt tijdens het bouwen van de blog een waarschuwing gemeld.

# Afbeeldingen

Het integreren van afbeeldingen in tekst gebeurt met de standaard Markdown-syntax. Afbeeldingen kunnen intern of extern zijn.

```
![Voorbeeld externe afbeelding](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Voorbeeld interne afbeelding](assets/img/got_wallpaper.jpg)
```

![Voorbeeld externe afbeelding](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Voorbeeld interne afbeelding](assets/img/got_wallpaper.jpg)

Standaard worden afbeeldingen weergegeven zodat ze de breedte van de tekst niet overschrijden en zijn ze altijd gecentreerd. Dit zorgt ervoor dat te grote afbeeldingen correct worden weergegeven, ook op smartphoneschermen.

Als een interne afbeelding in tekst wordt gebruikt maar niet bestaat, wordt tijdens het bouwen van de blog een waarschuwing gemeld.

# Het ontwerp van Pureblog aanpassen (geavanceerd)

De configuratie van je Pureblog steunt op het configuratiebestand. Standaard staat het configuratiebestand in `config/config.yml`. Dit configuratiebestand bevat een sectie `theme` die naar twee bestanden verwijst. Met deze bestanden kun je het ontwerp van je Pureblog aanpassen.

Het templatebestand (`theme.template_file`) is een HTML-bestand dat de algemene structuur van een Pureblog-pagina definieert. Je kunt het aanpassen om de algemene paginastructuur te wijzigen.

Het templatebestand bevat parameters die tijdens de bouw van de site worden vervangen. De beschikbare parameters in het template zijn:

- `$lang`: de taalcode van de huidige pagina.
- `$description`: de samenvatting van de pagina zoals beschreven in de front matter van een blogbericht (`excerpt`).
- `$root`: het relatieve pad naar de buildroot vanaf de huidige pagina (bv. `..` voor een hoofdpagina van een taal, `../..` voor een blogberichtpagina). Deze parameter wordt gebruikt als prefix voor URLs zodat de weergave correct verloopt.
- `$site_title`: de titel van de site zoals gedefinieerd in de configuratie (`general.site_title`).
- `$title`: de paginatitel zoals gedefinieerd in de front matter van een blogbericht (`title`).
- `$lang_switcher`: het blok waarmee de bezoeker op een pagina van taal kan wisselen.
- `$content`: de inhoud, gerenderd als HTML.
- `$author`: de auteur zoals gedefinieerd in de configuratie (`general.author`). Deze wordt in de voettekst weergegeven als `© {auteur} {jaar}`.
- `$year`: het jaar van de laatste build van de website.

Wijzigingen aan de visuele stijl kunnen worden doorgevoerd in de stylesheet. Het stijlbestand (`theme.style_file`) is een CSS-bestand dat de opmaakregels voor de verschillende elementen van de site definieert.

## Favicon op basis van een emoji

De favicon is het kleine icoontje dat in browsertabbladen, bladwijzers en zoekresultaten naast de naam van je site wordt weergegeven. Pureblog genereert het automatisch op basis van één enkele emoji die is ingesteld in `config/config.yml`:

```yaml
theme:
  favicon_emoji: "🤍"
```

Vervang de emoji door elk gewenst teken — een hart, een camera, een raket — om je blog een onderscheidende identiteit te geven. De wijziging is van kracht na de volgende build.

**Waarom een emoji in plaats van een PNG- of ICO-bestand?**

Traditionele favicons vereisen speciale beeldbewerkingstools, meerdere resoluties (16×16, 32×32, 180×180…) en meerdere kilobytes aan bestanden. Pureblog kiest voor een eenvoudigere aanpak:

- **Geen tools nodig.** Een emoji is gewoon een tekstteken: pas de configuratie aan, bouw opnieuw, klaar.
- **Vectorformaat.** De emoji wordt als SVG gerenderd, waardoor het op elke grootte en schermresolutie perfect scherp is, inclusief HiDPI- en Retina-schermen.
- **Geen gewicht.** De gegenereerde SVG is slechts een paar honderd bytes groot, vergeleken met tientallen kilobytes voor een klassieke iconenset.
- **Directe persoonlijkheid.** Eén teken is genoeg om het tabblad onmiskenbaar van jou te maken.

Het gegenereerde bestand `favicon.svg` wordt in de rootmap van de build geplaatst en op elke pagina — inclusief de root-redirectpagina — via een `<link rel="icon">`-tag gerefereerd. De referentie gebruikt een absolute URL afgeleid van `general.site_url`, zodat feedlezers zoals Inoreader het icoon correct oplossen en weergeven. Alle moderne browsers ondersteunen SVG-favicons.

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
