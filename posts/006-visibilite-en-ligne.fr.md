---
title: Visibilité en ligne
date: 2026-05-01
excerpt: Pureblog intègre de base un ensemble de mécanisme pour améliorer la visibilité de votre Pureblog sur les moteurs de recherche et dans les LLMs. Découvrez les solutions mises en place telles que les balises SEO (Search Engine Optimization), les sitemaps et les flux RSS.
---

La visibilité de votre contenu en ligne est un point clé à ne pas négliger si vous souhaitez construire votre audience ou plus simplement partager vos réflexions. Pureblog a été conçu dès le départ pour permettre un bon référencement de votre contenu sur les moteurs de recherches (Google, Bing, etc) et dans les LLMs (ChatGPT, Claude, Gemini, etc).

Cette page explique les mesures et les fonctionnalités intégrées à Pureblog afin d'améliorer la visibilité de votre site.

## Back to the basics

SEO = speed, structuration du contenu, facilité de parsing pour les LLMs, la description en meta data.

## La séparation entre le titre et l'URL

TODO

## Le sitemap

TODO

## Les flux RSS

Le flux RSS (Really Simple Syndication) est un format de fichier XML qui permet de syndiquer et de diffuser automatiquement des contenus web (articles, actualités, podcasts) fréquemment mis à jour. Il permet aux utilisateurs de s'abonner à leurs sites favoris et de recevoir les nouvelles mises à jour sans avoir à visiter chaque site individuellement.

Les utilisateurs peuvent consulter les dernières publications sous forme de résumés ou de textes intégraux via des lecteurs dédiés comme Feedly, Inoreader ou encore des extensions de navigateur.

Pureblog fournit un flux RSS par langue. Les flux RSS sont générés automatiquement lors de la génération de votre site. Les flux RSS sont disponibles via des URLs de cette forme : `https://www.example.com/<lang>/feed.xml`.

Pour la langue que vous être en train de lire sur ce site, le flux RSS est disponible sur <https://www.pureblog.dev/fr/feed.xml>.

Les flux RSS sont toujours composés d'un ensemble d'articles.

Chaque article contient :

- Un titre défini dans l'entête de votre article (tag `title`)
- Une description définie dans l'entête de votre article (tag `excerpt`). Si ce tag n'est pas défini, Pureblog utilise automatiquement les 200 premiers caractères de votre article.
- Le moment de publication qui est composé de la date dans l'entête de votre article (tag `date`) et la configuration (`publish.default_timezone` et `publish.default_publish_hour`).
- Un lien permanent qui se base sur le nom du fichier de votre article (le fameux `slug`). ⚠️ Il est important de ne pas trop changer ces _slugs_ sous peine de référencer dans les moteurs de recherche des articles qui n'existent plus.

## Les fichiers de configuration pour les moteurs de recherches et les LLMs

robots.txt et llms.txt
