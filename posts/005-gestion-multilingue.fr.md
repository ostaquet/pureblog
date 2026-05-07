---
title: Gestion multilingue
date: 2026-05-02
excerpt: L'intégration multilingue est un point clé de Pureblog. Découvrez en quoi Pureblog est différent et comment les langues sont gérés pour assurer la meilleure expérience utilisateur et le meilleur référencement.
---

Pureblog est avant tout un moteur de blog multilingue. Il a été créé après avoir fait de nombreux essais avec des solutions existantes (WordPress, Ghost, Bearblog, Drupal, Chirpy/Jekyll). A chaque tentative, la gestion multilingue relevait plus du bidouillage que de la gestion intégrée dans le moteur. Les bidouilles fonctionnent d'un point de vue visuel pour le visiteur mais ont un impact négatif sur le référencement et l'expérience utilisateur dans la cas d'un usage avec un flux RSS.

## Les pages d'accueil et les indexes

Les pages d'accueil des différentes langues sont différenciées par une extension de l'URL. Ceci permet de garder un flux RSS par langue afin que le visiteur puisse lire les articles de votre Pureblog dans sa langue préférée.

Typiquement, le Pureblog que vous êtes en train de lire est disponible dans plusieurs langues. Il existe donc plusieurs URLs permettant d'accéder aux indexes:

- <https://www.pureblog.dev/en>
- <https://www.pureblog.dev/fr>
- <https://www.pureblog.dev/nl>
- ...

Les différentes langues sont définies dans le fichier de configuration `config/config.yml` sous le paramètre `languages.codes`. La première langue définie est toujours la langue par défaut.

La langue par défaut est utilisée pour faire une redirection à partir de l'URL de base de votre Pureblog. Pour ce Pureblog, la langue par défaut est `en` (anglais). Donc, le visiteur qui ouvre l'URL <https://www.pureblog.dev> se voit automatiquement redirigé vers <https://www.pureblog.dev/en>.

Toutes les pages de votre Pureblog contiennent un sélecteur de langue (_language switcher_); y compris les pages d'acceuil. Ce sélecteur permet au visiteur de basculer rapidement sur la langue de son choix.

## Les flux RSS et le sitemap

Chaque langue possède son propre flux RSS. Ceci permet au visiteur de suivre les articles de votre Pureblog dans sa langue favorite. Les flux RSS sont toujours attachés sous une URL de langue de la manière <https://www.pureblog.dev/fr/feed.xml>.

Le sitemap est unique pour l'intégralité du site. Il contient les pages d'accueil et les articles. Pour chaque page, le sitemap mentionne la langue et les langues alternatives disponibles pour la page ainsi que les URLs. C'est souvent sur ce point que les autres moteurs de blog pèchent car ils ne gèrent pas les liens alternatifs entre les articles dans le sitemap.

Pour en savoir plus sur les flux RSS et les sitemaps, consultez [la page sur la visibilité en ligne](posts/006-visibilite-en-ligne.fr.md).

## Les liens entre les langues pour un même article

Pour améliorer le référencement, un article peut avoir une URL différentiée selon la langue. C'est également une différence par rapport aux moteurs de blog traditionels.

L'URL est toujours composée à partir du nom de fichier de l'article. Le nom de fichier est composée par `<id>-<slug>.<lang>.md`. L'identifiant id permet de faire le lien avec une même page écrite dans différentes langues. Le `slug` est l'URL qui sera utilisée. La langue est le code ISO en 2 caractères (`lang`). Donc, un fichier portant le nom `002-ecrire-nouvel-article.fr.md` sera référencée sur l'URL `fr/ecrire-nouvel-article`.

Un article écrit en plusieurs langue peut avoir des URLs différenciées par langue. Par exemple :

- `002-write-new-post.en.md` pour l'anglais.
- `002-ecrire-nouvel-article.fr.md` pour le français.
- `002-schrijf-nieuw-bericht.nl.md` pour le néerlandais.
- ...

L'identifiant sert de connecteur entre les différentes langues du même article (dans l'exemple, l'identifiant est `002`).

Comme indiqué plus haut, chaque page de votre Pureblog contient un sélecteur de langue. Ce sélecteur est clairement visible pour permettre au visiteur de lire l'article dans une autre langue. Si l'article n'est pas disponible dans une langue, le sélecteur indique le code langue barré (exemple : ~~NL~~ ). Si le visiteur clique quand même sur le lien barré, il est redirigé vers la page actuelle.

Lorsqu'un article existe dans une langue mais pas dans les autres, un avertissement d'affiche lors de la génération du site.

## La configuration des langues

Les langues disponibles sont indiquées dans le fichier de configuration `config/config.yml` dans la section `languages`. Cette section contient un ensemble de paramètres permettant d'ajuster la configuration des langues.

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

Les codes langues sont indiqués dans le paramètre `languages.codes`. Les codes langues sont mentionnés en [ISO 639-1](https://fr.wikipedia.org/wiki/Liste_des_codes_ISO_639-1) (codes langues en 2 lettres).

Le premier code langue est la langue par défaut de votre Pureblog.

Les paramètres `languages.reading_time_labels` et `languages.back_labels` sont les libellés qui sont utilisés lors de la génération du site pour indiquer le nombre de minutes de lecture d'un article et le libellé de retour à la page d'accueil.

## Que se passe t'il si un article existe dans une seule langue ?

Les pages d'accueil, le sitemap et les flux RSS se basent exclusivement sur la présence des fichiers d'articles. Donc, si un fichier n'existe pas (la version NL par exemple), l'article n'apparaît nulle part sur votre Pureblog.

Si l'article n'est pas disponible dans une langue, le sélecteur de langue indique le code langue barré (exemple : ~~NL~~ ). Si le visiteur clique quand même sur le lien barré, il est redirigé vers la page actuelle.

Lorsqu'un article existe dans une langue mais pas dans les autres, un avertissement d'affiche lors de la génération du site.

## Est-ce que Pureblog fonctionne pour une seule langue ?

Oui, Pureblog peut être utilisé avec une seule langue. Dans ce cas, il suffit d'indiquer un seul code langue dans le fichier de configuration (`languages.codes`).

Il faut noter que le comportement de redirection reste identique. Si vous utilisez uniquement le code langue `en`, la page d'accueil `https://www.example.com` sera quand même redirigée vers `https://www.example.com/en`. Ceci permet d'ajouter des langues plus tard et de commencer avec un Pureblog mono-langue.

Lorsqu'une seule langue est configurée, le sélecteur de langue ne s'affiche pas sur les pages d'accueil et sur les pages d'articles. Dans l'esprit minimaliste, il est inutile de surcharger la page avec un sélecteur devenu inutile.
