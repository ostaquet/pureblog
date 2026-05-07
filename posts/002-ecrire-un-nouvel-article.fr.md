---
title: Ecrire un nouvel article de blog
date: 2026-05-04
excerpt: Ce tutoriel vous guidera sur la façon d'écrire un article sur votre Pureblog, et il vaut la peine d'être lu même si vous avez utilisé d'autres moteurs de blog auparavant.
---

Ce tutoriel vous guidera sur la façon d'écrire un article sur votre Pureblog.

## Convention de nommage et dossiers

Par défaut, les articles de votre Pureblog se trouvent dans le dossier `posts/`.

Créez un nouveau fichier nommé `<id>-<slug>.<lang>.md`. Par exemple : `042-premier-article.fr.md`.

## Entête

Votre article se compose d'un entête qui sera utile au référencement et à la structure de votre site. Remplissez l'entête avec les lignes ci-dessous :

```
---
title: Mon premier article
date: 2026-05-07
---
```

## Date de publication

Par souci de simplicité, Pureblog utilise uniquement la date pour les articles. Vu que les flux RSS nécessitent également l'heure et le fuseau horaire, ces derniers sont configurés dans le fichier de configuration (section `publish`).

## Description de l'article

Par défaut, les 200 premiers mots de l'article sont utilisés comme description sur la page d'accueil, dans le flux RSS et dans les balises pour le référencement. Si vous désirez définir manuellement la description, vous pouvez la personnaliser avec le tag `excerpt` dans l'entête.

Par exemple :

```
---
title: Mon premier article
date: 2026-05-07
excerpt: Ceci est mon premier article sur Pureblog
---
```

## Contenu

Après l'entête, vous êtes libre d'écrire le contenu que vous voulez. La mise en page et les différentes typographies sont décrites dans la [page concernant le design](posts/004-design-mise-en-page-et-typographie.fr.md).

## Rédaction de l'article dans les autres langues

Vous pouvez maintenant rédiger votre article dans les autres langues en anglais et en néerlandais. La seule règle à respecter est que l'identifiant soit identique.

Donc, vous pouvez créer les articles `042-first-post.en.md` et `042-eerst-bericht.nl.md`. Ils seront automatiquement lié à votre premier article comme traductions.

Vous trouverez plus de [détails concernant la gestion multilingue sur la page dédiée](posts/005-gestion-multilingue.fr.md).
