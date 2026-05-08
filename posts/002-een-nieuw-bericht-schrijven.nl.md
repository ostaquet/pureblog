---
title: Een nieuw blogbericht schrijven
date: 2026-05-04
excerpt: Deze tutorial begeleidt je bij het schrijven van een bericht op je Pureblog, en is het lezen waard, zelfs als je eerder andere blogengines hebt gebruikt.
---

Deze tutorial begeleidt je bij het schrijven van een bericht op je Pureblog.

## Naamgevingsconventie en mappen

Standaard staan de berichten van je Pureblog in de map `posts/`.

Maak een nieuw bestand aan met de naam `<id>-<slug>.<lang>.md`. Bijvoorbeeld: `042-eerst-bericht.nl.md`.

## Front matter

Je bericht begint met een header die helpt voor SEO en de structuur van je site. Vul de front matter in met de onderstaande regels:

```
---
title: Mijn eerste bericht
date: 2026-05-07
---
```

## Publicatiedatum

Voor de eenvoud gebruikt Pureblog enkel de datum voor berichten. Aangezien RSS-feeds ook tijd en tijdzone vereisen, worden die geconfigureerd in het configuratiebestand (sectie `publish`). De standaardtijdzone is `Europe/Brussels` (configureerbaar via `publish.default_timezone`) en de zomertijd wordt automatisch beheerd.

## Berichtbeschrijving

Standaard worden de eerste 200 tekens van het bericht gebruikt als beschrijving op de startpagina, in de RSS-feed en in de SEO-metatags. Wil je de beschrijving handmatig instellen, dan kun je deze aanpassen met de `excerpt`-tag in de front matter.

Bijvoorbeeld:

```
---
title: Mijn eerste bericht
date: 2026-05-07
excerpt: Dit is mijn eerste bericht op Pureblog
---
```

## Inhoud

Na de front matter ben je vrij om de inhoud te schrijven die je wilt. De opmaak en de verschillende typografische opties worden beschreven op de [pagina over ontwerp](posts/004-ontwerp-opmaak-en-typografie.nl.md).

## Leestijd

Pureblog berekent automatisch een geschatte leestijd voor elk bericht (aan 200 woorden per minuut, met een minimum van één minuut). Deze tijd wordt naast de datum getoond, zowel op de startpagina als op de berichtpagina. Het bijbehorende label (bv. "min leestijd" in het Nederlands) wordt per taal geconfigureerd in `languages.reading_time_labels` van het configuratiebestand.

## Het bericht in andere talen schrijven

Je kunt je bericht nu in andere talen schrijven, zoals Frans en Engels. De enige regel die je moet volgen is dat de identificatie identiek moet zijn.

Je kunt dus de berichten `042-premier-article.fr.md` en `042-first-post.en.md` aanmaken. Ze worden automatisch als vertalingen gekoppeld aan je eerste bericht.

Meer [details over meertalig beheer vind je op de gewijde pagina](posts/005-meertalig-beheer.nl.md).
