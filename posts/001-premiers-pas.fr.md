---
title: Premiers pas
date: 2026-05-05
excerpt: Pureblog est un moteur de blog statique et minimaliste avec la meilleure gestion de contenu multilingue. Découvrez les bases de Pureblog dans cette vue d'ensemble. Vous apprendrez comment installer, configurer et utiliser votre premier site web basé sur Pureblog, ainsi que le déployer sur un serveur web.
---

## Qu'est-ce que Pureblog ?

Pureblog est un moteur de blog statique et minimaliste avec un support amélioré pour les contenus rédigés en plusieurs langues. Pureblog convertit des contenus écrits en Markdown vers un site web statique.

Il n'a aucun trackers et aucune ligne de Javascript. Le design est volontairement minimaliste. De par sa conception, Pureblog est extrêmement rapide et requiert très peu de ressources système pour héberger votre blog même si vous avez un trafic important.

**La seule chose qui compte vraiment, c'est votre contenu.**

## Préparer votre propre dépôt Pureblog

Pour commencer à construire votre propre Pureblog, il vous suffit de faire un _fork_ du dépôt (_repository_) principal de Pureblog.

Pour ce faire :

1. Connectez-vous avec votre compte GitHub sur <https://github.com/ostaquet/pureblog>
2. Cliquez sur le bouton **Fork** en haut à droite.
3. Choisissez un nom de dépôt (par exemple : `my-pureblog` avec pour propriétaire `ostaquet`).
4. Cliquez sur **Create fork**.
5. Copiez-collez l'URL GitHub de votre dépôt (par exemple `https://github.com/ostaquet/my-pureblog`).

Vous avez maintenant un dépôt Pureblog dans votre espace GitHub.

## Mettre en place l'environnement

Assurez-vous d'avoir les éléments nécessaires pour l'utilisation de Pureblog sur votre machine. Concrètement, vous avez besoin de Git, Python 3.13+ et Make.

Ouvrez un terminal pour vous assurer que Git, Python et Make sont installés avec les commandes suivantes :

```
git --version
python3 --version
make --version
```

Si les programmes sont bien installés, vous devriez avoir la version actuellement installée sur votre machine. Si vous avez un message d'erreur, vous devez installer les programmes manquants.

Effectuez un clone de votre dépôt en local avec la commande :

```
git clone https://github.com/<proprietaire>/<nom-du-depot>
```

Dans notre exemple, il s'agit de `git clone https://github.com/ostaquet/my-pureblog`.

Vous avez maintenant un clone local, il ne reste plus qu'à lancer le Pureblog de test.

Allez dans le dossier contenant le clone de votre dépôt :

```
cd <nom-du-depot>
```

Dans notre exemple, il s'agit de `cd my-pureblog`.

Lancez le service en local :

```
make serve
```

Le système va installer les dépendances et lancer une génération du Pureblog que vous êtes en train de lire.

Vous pouvez maintenant aller sur <http://localhost:8000> pour naviguer sur le Pureblog qui est sur votre ordinateur.

## Utilisation et configuration

Dans votre Pureblog, il y a quelques éléments à savoir.

La configuration se trouve dans le fichier `config/config.yml`. Le fichier est bien documenté pour vous permettre d'adapter la configuration à vos besoins.

Tous les champs sont obligatoires. La génération s'interrompt avec une erreur explicative si un champ est manquant ou invalide (par exemple, une traduction manquante pour une langue déclarée, ou un fuseau horaire inconnu).

Pour utiliser un fichier de configuration différent, passez-le via `--config` :

```
python3 src/main.py --config path/to/your-config.yml
```

Vous pouvez également utiliser la commande suivante pour générer votre Pureblog avec le fichier de configuration par défaut `config/config.yml` :

```
make build
```

Ou encore lancer la génération et un serveur HTTP pour visualiser le résultat sur <http://localhost:8000> :

```
make serve
```

### Sections du fichier de configuration

Le fichier `config/config.yml` est organisé en cinq sections, toutes obligatoires :

- `general` : titre du site, URL du site, auteur (affiché dans le pied de page sous la forme `© {auteur} {année}`), dossier des articles, dossier de sortie et dossier des ressources statiques.
- `seo` : chemin vers le fichier source `robots.txt`.
- `languages` : liste des codes de langues et libellés localisés (temps de lecture, lien de retour).
- `publish` : fuseau horaire et heure de publication par défaut, utilisés pour les dates des flux RSS.
- `theme` : chemins vers le template HTML et la feuille de style CSS, ainsi que `favicon_emoji` (un seul emoji, par exemple `📝`, qui est converti en SVG et exposé à `/favicon.svg`).

Par défaut, les articles de blogs se trouvent dans `posts/`. Les articles de blog sont des fichiers Markdown (`.md`). Le nom de fichier est composée par `<id>-<slug>.<lang>.md`. L'identifiant id permet de faire le lien avec une même page écrite dans différentes langues. Le `slug` est l'URL qui sera utilisée. La langue est le code ISO en 2 caractères (`lang`).

Les ressources statiques (images, etc.) se trouvent dans le répertoire configuré par `general.assets_dir` (par défaut : `assets/`). L'ensemble du répertoire est copié textuellement dans `build/assets/` à chaque génération, de sorte que les images internes peuvent être référencées depuis les articles en utilisant leur chemin relatif.

N'hésitez pas à lire l'article concernant [la rédaction d'un nouvel article](posts/002-ecrire-un-nouvel-article.fr.md) pour vous familiariser avec Pureblog.

⚠️ **Important** ⚠️ : Lorsque vous travaillez sur la rédaction de vos articles, ils ne sont pas rafraîchis automatiquement dans le navigateur. En effet, les articles sont générés en HTML statique. Donc, vous devez relancer un `make build` ou un `make serve` pour les regénérer après un changement.

Pour repartir d'une génération propre, vous pouvez supprimer le dossier de sortie avec `make clean`.

## Publier votre Pureblog sur Internet

Votre Pureblog est prêt à être publié dans le dossier `build/`. Lorsque vous copiez-collez l'intégralité de ce contenu sur un serveur web, vous pouvez immédiatement naviguer sur vos pages.

Le dossier de sortie du site généré est configurable dans le fichier de configuration (`general.build_dir`).

⚠️ **Avant le déploiement**, modifiez `general.site_url` dans `config/config.yml` pour qu'il pointe vers votre vrai nom de domaine. Cette URL est utilisée dans les flux RSS et le sitemap : si elle n'est pas correcte, les liens absolus de votre site pointeront vers un mauvais domaine.
