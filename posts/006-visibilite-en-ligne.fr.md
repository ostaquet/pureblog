---
title: Visibilité en ligne
date: 2026-05-01
excerpt: Pureblog intègre de base un ensemble de mécanisme pour améliorer la visibilité de votre Pureblog sur les moteurs de recherche et dans les LLMs. Découvrez les solutions mises en place telles que les balises SEO (Search Engine Optimization), les sitemaps et les flux RSS.
---

La visibilité de votre contenu en ligne est un point clé à ne pas négliger si vous souhaitez construire votre audience ou plus humblement partager vos réflexions. Pureblog a été conçu dès le départ pour permettre le meilleur référencement de votre contenu sur les moteurs de recherches (Google, Bing, etc) et sur les LLMs (ChatGPT, Claude, Gemini, etc).

Cette page explique les fonctionnalités intégrées à Pureblog qui améliore la visibilité de votre contenu.

## Les signaux web essentiels (_back to the basics_)

Les signaux web essentiels (_Core Web Vitals_) sont des métriques Google évaluant l'expérience utilisateur réelle d'un site web via la vitesse de chargement (_LCP_), la réactivité (_INP_) et la stabilité visuelle (_CLS_). Ils sont essentiels pour le SEO (_Search Engine Optimization_ ou facteurs de classement), ils ciblent des seuils spécifiques, notamment un _LCP_ ≤ 2,5 s, un _INP_ ≤ 200 ms et un _CLS_ ≤ 0,1, analysés dans la [Google Search Console](https://search.google.com/search-console).

Les 3 signaux web essentiels (_Core Web Vitals_) sont les suivants :

- **La vitesse de chargement** ou [LCP (Largest Contentful Paint)](https://web.dev/articles/lcp?hl=fr) : Il s'agit de la mesure du temps nécessaire pour afficher le plus grand élément visible (image, bloc de texte) à l'écran. Un bon LCP est inférieur ou égal à 2,5 secondes.
- **La réactivité lors de l'interaction** ou [INP (Interaction to Next Paint)](https://web.dev/articles/inp?hl=fr) : Il s'agit de la mesure de la latence de toutes les interactions de l'utilisateur (clics, appuis). La mesure se base sur la pire interaction. Il remplace le _FID (First Input Delay)_ depuis mars 2024, avec un objectif cible de 200 millisecondes ou moins.
- **La stabilité visuelle** ou [CLS (Cumulative Layout Shift)](https://web.dev/articles/cls?hl=fr) : Il s'agit de la mesure des changements de mise en page inattendus. Le score doit être inférieur ou égal à 0,1 pour garantir une navigation stable.

Ces éléments sont pris en charge par Pureblog de deux manières :

1. L'intégralité de votre Pureblog est en HTML statique. C'est-à-dire qu'il est construit lors de la génération. Les pages sont légères et ne nécessitent aucun post-traitement dans le navigateur du visiteur. Cela signifie que le _LCP_ et le _INP_ restent extrêmement bas même si vous avez beaucoup de contenu.
2. Toutes les pages ont un format unique basée sur un template dont vous avez le contrôle. Le template assure une cohérence au sein de votre Pureblog, tout en étant personnalisable (voir aussi [comment modifier le design de votre Pureblog](posts/004-design-mise-en-page-et-typographie.fr.md)).

**TODO AJOUTER UN SCREENSHOT DES CORE VITALS DE CE SITE UNE FOIS PUBLIE**

## Les éléments clés du référencement

Tous les éléments clés du référencement sont gérés dans Pureblog.

Lorsque vous observez attentivement un résultat de recherche Google, vous trouvez les éléments clés suivants :

- Le titre du site
- L'icône (_favicon_)
- L'URL
- Le titre de la page
- La description de la page

![Description de l'anatomie d'un résultat Google](assets/img/anatomie_google_entry_fr.png)

Le titre du site est défini dans le fichier de configuration (`config/config.yml`) avec le paramètre `general.site_title`.

L'icône du site (favicon) est générée automatiquement par Pureblog à partir d'un simple emoji défini dans le paramètre `theme.favicon_emoji` du fichier de configuration (par exemple `📝`). Pureblog produit un fichier SVG accessible à `/favicon.svg` et le référence sur toutes les pages du site, sans qu'aucune ressource graphique externe ne soit requise.

L'URL est définie par le `slug` de la page et le code langue. Le `slug` est obtenu à partir du nom du fichier Markdown. Le `slug` est important pour le référencement.

Le titre et la description de la page sont définis dans l'entête de l'article respectivement avec les tags `title` et `excerpt`.

Chaque article de blog possède une description (`excerpt` dans l'entête de votre article). Cette description est générée automatiquement en utilisant les 200 premiers caractères de votre article si elle n'est pas définie. La description est utilisée dans la balise meta de vos pages d'article (`<meta name="description" content="..."/>`).

## La séparation entre le titre et l'URL

De nombreux blog utilisent le titre de la page comme URL. Nous pensons que c'est une mauvaise idée. En effet, le titre de la page peut contenir des mots "vides" (comme des "un", "les", etc). Or, l'URL ne nécessite pas ces mots "vides". L'URL doit être la plus courte possible et contenir les mots clés utiles au référencement. De plus, un changement dans le titre de la page pour une correction ne devrait pas casser les URLs déjà référencées sur d'autres sites ou dans les moteurs de recherche.

C'est pour cela que le titre de la page et l'URL sont deux notions différenciées dans Pureblog.

Le titre de la page (qui est repris dans la page et qui est visible pour les visiteurs) est défini dans l'entête de l'article (sous le tag `title`). C'est également ce titre qui est utilisé pour construire les indexes reprennant toutes les pages du site.

L'URL, quant à elle, est composée à partir du nom de fichier de l'article. Le nom de fichier est composé par `<id>-<slug>.<lang>.md`. L'identifiant `id` permet de faire le lien avec une même page écrite dans différentes langues. Le `slug` est l'URL qui sera utilisée. La langue est le code ISO en 2 caractères (`lang`).

Donc, un fichier portant le nom `002-ecrire-nouvel-article.fr.md` sera référencé sur l'URL `/fr/ecrire-nouvel-article/`.

## Le sitemap

Un sitemap (plan de site) est un fichier XML répertoriant les pages, vidéos et fichiers essentiels d'un site web pour les moteurs de recherche. Il agit comme une carte, facilitant le travail des robots d'indexation (crawl) pour découvrir et indexer efficacement le contenu, notamment pour les nouveaux sites ou les structures complexes.

Pour un blog, il permet également de s'assurer que toutes les pages sont référencées; même celles qui ne se trouvent plus sur la page principale du site (sur une 2e ou 3e page par exemple).

Pourquoi le sitemap est-il important ?

- **Indexation rapide et complète** : Il permet à Google et aux autres moteurs de trouver rapidement toutes les pages, même celles peu reliées entre elles (maillage faible).
- **Mises à jour signalées** : Il indique aux robots la dernière date de modification des pages, les incitant à revenir pour actualiser l'index.
- **Optimisation SEO** : Il aide à mieux faire comprendre la structure du site et à indexer des contenus spécifiques (vidéos, images, actualités).
- **Indispensable pour certains sites** : Crucial pour les grands sites, les sites récents avec peu de liens externes, ou ceux utilisant beaucoup de contenu riche (vidéo)

Pureblog génère automatiquement un fichier sitemap pour l'ensemble de votre Pureblog en tenant compte des traductions et de la disponibilité des différentes langues. Pour chaque page, la date de dernière modification (`<lastmod>`) est tirée de la date de l'article ; pour les pages d'index, c'est la date de l'article le plus récent dans la langue concernée qui est utilisée.

Le fichier sitemap est disponible à l'URL <https://www.example.com/sitemap.xml> et il est référencé automatiquement dans le `robots.txt` pour faciliter sa découverte par les crawlers (moteur de recherche et LLMs).

Exemple de sitemap pour ce Pureblog : <https://www.pureblog.dev/sitemap.xml>.

## Les flux RSS

Le flux RSS (_Really Simple Syndication_) est un format de fichier XML qui permet de syndiquer et de diffuser automatiquement des contenus web (articles, actualités, podcasts) fréquemment mis à jour. Il permet aux utilisateurs de s'abonner à leurs sites favoris et de recevoir les nouvelles mises à jour sans avoir à visiter chaque site individuellement.

Les utilisateurs peuvent consulter les dernières publications sous forme de résumés ou de textes intégraux via des lecteurs dédiés comme [Feedly](https://feedly.com/), [Inoreader](https://www.inoreader.com/fr/) ou encore des extensions de navigateur.

Pureblog fournit un flux RSS par langue. Les flux RSS sont générés automatiquement lors de la génération de votre Pureblog. Les flux RSS sont disponibles via des URLs sous la forme `https://www.example.com/<lang>/feed.xml`.

Pour la langue que vous êtes en train de lire sur ce site, le flux RSS est disponible sur <https://www.pureblog.dev/fr/feed.xml> et il est référencé sur chaque page dans une balise `<link>` d'autodécouverte (_RSS autodiscovery_) pour assurer sa découverte aisée par les applications tierces.

Un flux RSS est toujours composé d'un ensemble d'articles.

Chaque article contient :

- Un titre défini dans l'entête de votre article (tag `title`)
- Une description définie dans l'entête de votre article (tag `excerpt`). Si ce tag n'est pas défini, Pureblog utilise automatiquement les 200 premiers caractères de votre article.
- Le moment de publication qui est composé de la date mentionnée dans l'entête de votre article (tag `date`) et la configuration (`publish.default_timezone` et `publish.default_publish_hour`).
- Un lien permanent qui se base sur le nom du fichier de votre article (le fameux `slug`). ⚠️ Il est important de ne pas trop changer ces _slugs_ sous peine d'impacter négativement le référencement dans les moteurs de recherche.

## Les fichiers de configuration pour les moteurs de recherches et les LLMs

Pureblog gère également un fichier de configuration supplémentaire pour les moteurs de recherche et les LLMs.

Le fichier `robots.txt` est un fichier texte placé à la racine d'un site web qui donne des instructions aux robots d'indexation (crawlers) sur les pages à explorer ou non. Il sert principalement à gérer le budget de crawl et à bloquer l'accès à des zones privées, mais n'empêche pas l'indexation si la page est liée ailleurs.

Pureblog se base sur le fichier `robots.txt` référencé dans la configuration (`config/config.yml`) sous le paramètre `seo.robots_file`. Lors de la génération, le fichier renseigné est copié dans le site final et la directive `Sitemap:` est ajoutée automatiquement à la fin (uniquement si elle n'est pas déjà présente). Vous pouvez donc gérer librement le contenu de votre `robots.txt` source sans craindre de doublon.

Le fichier `robots.txt` est disponible à l'URL <https://www.pureblog.dev/robots.txt>.

## Page 404 personnalisée

Lorsqu'un visiteur arrive sur une URL inexistante de votre site, il voit une erreur 404. Par défaut, les hébergeurs affichent une page d'erreur brute, sans mise en forme. Pureblog génère automatiquement un fichier `404.html` à la racine du site, qui reproduit l'identité visuelle de votre blog. Le visiteur reste ainsi dans un environnement cohérent et peut retrouver facilement le chemin vers la page d'accueil.

La page est entièrement autonome : la feuille de style est intégrée directement dans le HTML et tous les liens utilisent l'URL absolue configurée dans `general.site_url`. Cela garantit que les styles et la navigation fonctionnent correctement quelle que soit la profondeur de l'URL à laquelle l'hébergeur sert la page d'erreur (par exemple, Firebase sert le même `404.html` que l'URL manquante soit `/brol` ou `/en/brol`).

La page affiche le message « page introuvable » dans la langue par défaut, ainsi qu'un lien vers la page d'accueil. Les deux textes se configurent dans `config/config.yml` sous la section `languages` :

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

Un sélecteur de langue est également intégré, avec des liens directs vers l'index de chaque langue configurée, afin que les visiteurs puissent naviguer même après avoir atterri sur une URL manquante.

Sur Firebase Hosting, le fichier `404.html` à la racine est servi automatiquement pour toute URL sans correspondance. Les autres hébergeurs statiques (Netlify, GitHub Pages, etc.) suivent la même convention.

## Autres fonctionnalités utiles

Pureblog est compatible avec les modes liseuses des navigateurs web sans altération de la mise en page.
