---
title: Eerste stappen
date: 2026-05-05
excerpt: Pureblog is een statische, minimalistische blogengine met het beste meertalige contentbeheer. Ontdek de basis van Pureblog in dit overzicht. Je leert hoe je je eerste op Pureblog gebaseerde website installeert, configureert en gebruikt, en hoe je deze op een webserver implementeert.
---

## Wat is Pureblog?

Pureblog is een statische, minimalistische blogengine met verbeterde ondersteuning voor inhoud die in meerdere talen is geschreven. Pureblog zet inhoud die in Markdown is geschreven om naar een statische website.

Het bevat geen trackers en geen enkele regel JavaScript. Het ontwerp is bewust minimalistisch. Door het ontwerp is Pureblog extreem snel en heeft het zeer weinig systeembronnen nodig om je blog te hosten, zelfs bij veel verkeer.

**Het enige wat echt telt, is je inhoud.**

## Je eigen Pureblog-repository voorbereiden

Om aan je eigen Pureblog te beginnen, hoef je alleen maar een _fork_ te maken van de hoofdrepository van Pureblog.

Daarvoor:

1. Meld je aan met je GitHub-account op <https://github.com/ostaquet/pureblog>
2. Klik op de knop **Fork** rechtsboven.
3. Kies een naam voor de repository (bijvoorbeeld: `my-pureblog` met `ostaquet` als eigenaar).
4. Klik op **Create fork**.
5. Kopieer de GitHub-URL van je repository (bijvoorbeeld `https://github.com/ostaquet/my-pureblog`).

Je hebt nu een Pureblog-repository in je GitHub-ruimte.

## De omgeving opzetten

Zorg ervoor dat je beschikt over wat nodig is om Pureblog op je machine te gebruiken. Concreet heb je Git, Python 3.13+ en Make nodig.

Open een terminal om te controleren of Git, Python en Make geïnstalleerd zijn met de volgende commando's:

```
git --version
python3 --version
make --version
```

Als de programma's correct zijn geïnstalleerd, zou je de versie moeten zien die op je machine geïnstalleerd is. Als je een foutmelding krijgt, moet je de ontbrekende programma's installeren.

Kloon je repository lokaal met het commando:

```
git clone https://github.com/<eigenaar>/<repo-naam>
```

In ons voorbeeld is dat `git clone https://github.com/ostaquet/my-pureblog`.

Je hebt nu een lokale kloon; het enige wat nog rest is de test-Pureblog te starten.

Ga naar de map met de kloon van je repository:

```
cd <repo-naam>
```

In ons voorbeeld is dat `cd my-pureblog`.

Start de service lokaal:

```
make serve
```

Het systeem zal de afhankelijkheden installeren en een build van de Pureblog die je nu leest activeren.

Je kunt nu naar <http://localhost:8000> gaan om door de Pureblog op je computer te bladeren.

## Gebruik en configuratie

Er zijn enkele dingen die je over je Pureblog moet weten.

De configuratie staat in het bestand `config/config.yml`. Het bestand is goed gedocumenteerd zodat je de configuratie aan je behoeften kunt aanpassen.

Alle velden zijn verplicht. De build stopt met een verklarende fout als een veld ontbreekt of ongeldig is (bijvoorbeeld een ontbrekende vertaling voor een opgegeven taal of een onbekende tijdzone).

Om een ander configuratiebestand te gebruiken, geef je het door via `--config`:

```
python3 src/main.py --config path/to/your-config.yml
```

Je kunt ook het volgende commando gebruiken om je Pureblog te bouwen met het standaard configuratiebestand `config/config.yml`:

```
make build
```

Of voer de build samen met een HTTP-server uit om het resultaat te bekijken op <http://localhost:8000>:

```
make serve
```

### Secties van het configuratiebestand

Het bestand `config/config.yml` is georganiseerd in vijf secties, die alle verplicht zijn:

- `general`: titel van de site, URL van de site, auteur (weergegeven in de voettekst als `© {auteur} {jaar}`), map met posts, uitvoermap en map met statische bronnen.
- `seo`: pad naar het bron-`robots.txt`-bestand.
- `languages`: lijst van taalcodes en gelokaliseerde labels (leestijd, terug-link).
- `publish`: tijdzone en standaardpublicatie-uur, gebruikt voor RSS-feeddatums.
- `theme`: paden naar het HTML-template en de CSS-stylesheet, evenals `favicon_emoji` (een enkele emoji, bv. `📝`, die wordt geconverteerd naar SVG en aangeboden op `/favicon.svg`).

Standaard staan de blogposts in `posts/`. Posts zijn Markdown-bestanden (`.md`). De bestandsnaam heeft de vorm `<id>-<slug>.<lang>.md`. De `id`-identificatie verbindt dezelfde pagina geschreven in verschillende talen. De `slug` is de URL die zal worden gebruikt. De taal is de ISO-code van 2 tekens (`lang`).

Statische bronnen (afbeeldingen, enz.) staan in de map die is geconfigureerd via `general.assets_dir` (standaard: `assets/`). De volledige map wordt bij elke build letterlijk gekopieerd naar `build/assets/`, zodat interne afbeeldingen vanuit posts kunnen worden gerefereerd via hun relatieve pad.

Lees gerust het artikel over [het schrijven van een nieuwe post](posts/002-een-nieuw-bericht-schrijven.nl.md) om vertrouwd te raken met Pureblog.

⚠️ **Belangrijk** ⚠️: Terwijl je je posts schrijft, worden ze niet automatisch ververst in de browser. Posts worden als statische HTML gegenereerd, dus moet je `make build` of `make serve` opnieuw uitvoeren om ze na een wijziging te regenereren.

Om vanuit een schone build te starten, kun je de uitvoermap verwijderen met `make clean`.

## Je Pureblog online publiceren

Je Pureblog is klaar om gepubliceerd te worden in de map `build/`. Wanneer je deze inhoud naar een webserver kopieert, kun je meteen door je pagina's bladeren.

De uitvoermap van de gegenereerde site is configureerbaar in het configuratiebestand (`general.build_dir`).

⚠️ **Voor de implementatie**, wijzig `general.site_url` in `config/config.yml` zodat het naar je echte domeinnaam wijst. Deze URL wordt gebruikt in RSS-feeds en de sitemap: als deze niet correct is, zullen de absolute links op je site naar het verkeerde domein wijzen.
