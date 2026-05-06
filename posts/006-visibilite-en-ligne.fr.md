---
title: Visibilité en ligne
date: 2026-05-01
excerpt: Pureblog intègre de base un ensemble de mécanisme pour améliorer la visibilité de votre Pureblog sur les moteurs de recherche et dans les LLMs. Découvrez les solutions mises en place telles que les balises SEO (Search Engine Optimization), les sitemaps et les flux RSS.
---

La visibilité de votre contenu en ligne est un point clé à ne pas négliger si vous souhaitez construire votre audience ou plus simplement partager vos réflexions. Pureblog a été conçu dès le départ pour permettre un bon référencement de votre contenu sur les moteurs de recherches (Google, Bing, etc) et dans les LLMs (ChatGPT, Claude, Gemini, etc).

Cette page explique les mesures et les fonctionnalités intégrées à Pureblog afin d'améliorer la visibilité de votre site.

## Les signaux web essientiels (back to the basics)

Les Core Web Vitals (Signaux Web essentiels) sont des métriques Google évaluant l'expérience utilisateur réelle d'un site web via la vitesse de chargement (LCP), la réactivité (INP) et la stabilité visuelle (CLS). Essentiels pour le SEO (facteurs de classement), ils ciblent des seuils spécifiques, notamment un LCP <= 2,5 s, un INP <= 200 ms et un CLS <= 0,1, analysés dans la [Search Console](https://search.google.com/search-console).

Les 3 Métriques Clés (Core Web Vitals):

- **Vitesse de chargement** ou [LCP (Largest Contentful Paint)](https://web.dev/articles/lcp?hl=fr) : Mesure le temps nécessaire pour afficher le plus grand élément visible (image, bloc de texte) à l'écran. Un bon LCP est inférieur ou égal à 2,5 secondes.
- **Réactivité lors de l'interaction** ou [INP (Interaction to Next Paint)](https://web.dev/articles/inp?hl=fr) : Mesure la latence de toutes les interactions de l'utilisateur (clics, appuis) et sélectionne la pire. Il remplace le FID depuis mars 2024, avec un objectif cible de 200 millisecondes ou moins.
- **Stabilité visuelle** ou [CLS (Cumulative Layout Shift)](https://web.dev/articles/cls?hl=fr) : Mesure les changements de mise en page inattendus. Le score doit être inférieur ou égal à 0,1 pour garantir une navigation stable

Ces 3 éléments sont pris en charge par Pureblog de deux manières.

1. L'intégralité de votre Pureblog est statique, cela signifie que le LCP et le INP sont extrêmement bas.
2. Toutes les pages ont un format unique basée sur le template HTML (voir aussi [comment modifier le design de votre Pureblog](posts/004-design-mise-en-page-et-typographie.fr.md)).

**TODO AJOUTER UN SCREENSHOT DES CORE VITALS DE CE SITE UNE FOIS PUBLIE**

## Les éléments clés du référencement

Tous les éléments clés du référencement sont gérés dans Pureblog.

![Description de l'anatomie d'un résultat Google](assets/img/anatomie_google_entry_fr.png)

Le titre du site est défini dans le fichier de configuration (`config/config.yml`) avec le paramètre `general.site_title`.

L'icône du site est définie par un emoji dans le fichier de configuration avec le paramètre `theme.favicon_emoji`.

L'URL est définie par le `slug` de la page et le code langue. Le `slug` est obtenu à partir du nom du fichier Markdown. Le `slug` est important pour le référencement.

Le titre et la description de la page sont définis dans l'entête de l'article respectivement avec les tags `title` et `excerpt`.

Chaque article de blog possède une description (`excerpt` dans l'entête de votre article). Cette description est générée automatiquement en utilisant les 200 premiers caractères de votre article si elle n'est pas définie. La description est utilisée dans le meta data de vos page d'article (`<meta name="description" content="xxx"/>`).

## La séparation entre le titre et l'URL

De nombreux blog utilisent le titre de la page comme URL. Nous pensons que c'est une mauvaise idée car cela peut impacter le référencement (si c'est bien utilisé) et surtout, un changement dans le titre de la page pour une correction ne devrait pas casser les URLs déjà référencées sur d'autres sites ou dans les moteurs de recherche.

C'est pour cela que le titre de la page et l'URL sont deux notions différenciées dans Pureblog.

Le titre de la page (qui est repris dans la page visible pour les visiteurs) est défini dans l'entête de l'article (sous le tag `title`). C'est également ce titre qui est utilisé pour construire les indexes reprennant toutes les pages du site.

L'URL est composée par le nom du fichier de l'article. Le nom du fichier est composée par `<id>-<slug>.<lang>.md`. L'identifiant `id` permet de faire le lien avec une même page écrite dans différentes langues. Le `slug` est l'URL qui sera utilisée. La langue est le code ISO en 2 caractères (`lang`).

Donc, un fichier portant le nom `002-ecrire-un-nouvel-article.fr.md` sera référencée sur l'URL `fr/ecrire-un-nouvel-article`.

## Le sitemap

Un sitemap (plan de site) est un fichier XML répertoriant les pages, vidéos et fichiers essentiels d'un site web pour les moteurs de recherche. Il agit comme une carte, facilitant le travail des robots d'indexation (crawl) pour découvrir et indexer efficacement le contenu, notamment pour les nouveaux sites ou les structures complexes.

Pour un blog, il permet également de s'assurer que toutes les pages sont référencées; même celles qui ne se trouvent pas sur la page principale du site (sur une 2e ou 2e page par exemple).

Pourquoi le sitemap est-il important ?

- **Indexation rapide et complète** : Il permet à Google et aux autres moteurs de trouver rapidement toutes les pages, même celles peu reliées entre elles (maillage faible).
- **Mises à jour signalées** : Il indique aux robots la dernière date de modification des pages, les incitant à revenir pour actualiser l'index.
- **Optimisation SEO** : Il aide à mieux faire comprendre la structure du site et à indexer des contenus spécifiques (vidéos, images, actualités).
- **Indispensable pour certains sites** : Crucial pour les grands sites, les sites récents avec peu de liens externes, ou ceux utilisant beaucoup de contenu riche (vidéo)

Pureblog génère automatiquement un fichier sitemap pour l'ensemble de votre Pureblog en tenant compte des traductions et de la disponibilité des différentes langues.

Le fichier sitemap est disponible à l'URL <https://www.pureblog.debv/sitemap.xml> et il est référencé automatiquement dans le `robots.txt` pour faciliter sa découverte par les crawlers (moteur de recherche et LLMs).

## Les flux RSS

Le flux RSS (Really Simple Syndication) est un format de fichier XML qui permet de syndiquer et de diffuser automatiquement des contenus web (articles, actualités, podcasts) fréquemment mis à jour. Il permet aux utilisateurs de s'abonner à leurs sites favoris et de recevoir les nouvelles mises à jour sans avoir à visiter chaque site individuellement.

Les utilisateurs peuvent consulter les dernières publications sous forme de résumés ou de textes intégraux via des lecteurs dédiés comme Feedly, Inoreader ou encore des extensions de navigateur.

Pureblog fournit un flux RSS par langue. Les flux RSS sont générés automatiquement lors de la génération de votre site. Les flux RSS sont disponibles via des URLs de cette forme : `https://www.example.com/<lang>/feed.xml`.

Pour la langue que vous être en train de lire sur ce site, le flux RSS est disponible sur <https://www.pureblog.dev/fr/feed.xml> et il est référencé sur chaque page dans une balise meta data pour assurer sa découverte aisée pour les applications tierces.

Les flux RSS sont toujours composés d'un ensemble d'articles.

Chaque article contient :

- Un titre défini dans l'entête de votre article (tag `title`)
- Une description définie dans l'entête de votre article (tag `excerpt`). Si ce tag n'est pas défini, Pureblog utilise automatiquement les 200 premiers caractères de votre article.
- Le moment de publication qui est composé de la date dans l'entête de votre article (tag `date`) et la configuration (`publish.default_timezone` et `publish.default_publish_hour`).
- Un lien permanent qui se base sur le nom du fichier de votre article (le fameux `slug`). ⚠️ Il est important de ne pas trop changer ces _slugs_ sous peine de référencer dans les moteurs de recherche des articles qui n'existent plus.

## Les fichiers de configuration pour les moteurs de recherches et les LLMs

Pureblog gère également un fichier de configuraton supplémentaire pour les moteurs de recherche et les LLMs.

Le fichier `robots.txt` est un fichier texte placé à la racine d'un site web qui donne des instructions aux robots d'indexation (crawlers) sur les pages à explorer ou non. Il sert principalement à gérer le budget de crawl et à bloquer l'accès à des zones privées, mais n'empêche pas l'indexation si la page est liée ailleurs.

Pureblog se base sur le fichier `robots.txt` référencé dans la configuration (`config/config.yml`) sous le paramètre `seo.robots_file`. Lors de la génération, le fichier renseigné est copié dans le site final est le lien vers le sitemap est ajouté automatiquement.

Le fichier `robots.txt` est disponible à l'URL <https://www.pureblog.dev/robots.txt>.

## Autres fonctionnalités utiles

Pureblog est compatible avec les modes liseuses des navigateurs web sans altération de la mise en page.
