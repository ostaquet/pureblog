---
title: Design, mise en page et typographie
date: 2026-05-03
excerpt: Quelques exemples de typographie, images et liens; ainsi que les fichiers clés pour adapter le design à votre goût.
---

Pureblog est conçu autour d'un design minimaliste permettant de couvrir les besoins dans le cadre d'une publication de blog posts.

# Exemples de typographie

## Titres et titres de sections

```
# Titre niveau 1
## Titre niveau 2
### Titre niveau 3
#### Titre niveau 4
```

# Titre niveau 1

## Titre niveau 2

### Titre niveau 3

#### Titre niveau 4

## Paragraphes et formatage

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar urna erat, et sollicitudin mi sodales id. Quisque sit amet egestas ex. Proin id diam ante. Duis varius porttitor luctus. Maecenas tempus nunc sed enim vehicula, sit amet laoreet turpis eleifend. Nunc vel sollicitudin neque. Quisque at laoreet metus. Proin sed odio nec urna eleifend interdum. Integer luctus magna nec neque consequat sagittis.
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar urna erat, et sollicitudin mi sodales id. Quisque sit amet egestas ex. Proin id diam ante. Duis varius porttitor luctus. Maecenas tempus nunc sed enim vehicula, sit amet laoreet turpis eleifend. Nunc vel sollicitudin neque. Quisque at laoreet metus. Proin sed odio nec urna eleifend interdum. Integer luctus magna nec neque consequat sagittis.

```
**Texte en gras**
_Texte en italique_
*Texte en italique*
~~Texte barré~~
`Ligne de code intégrée`
> Citation
```

**Texte en gras**

_Texte en italique_

_Texte en italique_

~~Texte barré~~

`Ligne de code intégrée`

> Citation

Les lignes vides séparent les paragraphes. Un simple saut de ligne à l'intérieur d'un paragraphe est converti en espace, conformément au comportement standard de Markdown.

Note : le texte barré (`~~…~~`) est volontairement ignoré à l'intérieur du code intégré (entre simples backticks) et des blocs de code (entre triples backticks), afin que les exemples de code restent rendus tels quels.

## Listes à puces

```
- Premier élément
- Deuxième élément
- Troisième élément
```

- Premier élément
- Deuxième élément
- Troisième élément

## Listes numérotées

```
1. Premier élément
2. Deuxième élément
3. Troisième élément
```

1. Premier élément
2. Deuxième élément
3. Troisième élément

## Code

Les lignes de code intégrées dans le texte :

```
`Ligne de code intégrée`
```

`Ligne de code intégrée`

Plusieurs lignes de code :

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

Il n'y a pas de saut automatique à la ligne lors de la mise en page de plusieurs lignes de code.

# Exemples de liens

Il existe 4 types de liens :

- Les liens automatiques (`<http://www.example.com>`)
- Les liens externes dans le même onglet (`[Ouvrir dans le même onglet](http://www.example.com)`)
- Les liens externes dans un nouvel onglet (`[Ouvrir dans un nouvel onglet](tab:http://www.example.com)`)
- Les liens internes dans le même onglet (`[Lien interne](posts/001-premiers-pas.fr.md)`)

Le préfixe `tab:` et les liens internes peuvent se combiner. Par exemple, `[Lien interne dans un nouvel onglet](tab:posts/001-premiers-pas.fr.md)` ouvre le lien interne résolu dans un nouvel onglet.

🔐 Note de sécurité : les liens ouverts dans un nouvel onglet (`tab:`) reçoivent automatiquement les attributs `target="_blank"` et `rel="noopener noreferrer"`, ce qui protège vos visiteurs contre le _tabnabbing_.

```
<http://www.example.com>
[Ouvrir dans le même onglet](http://www.example.com)
[Ouvrir dans un nouvel onglet](tab:http://www.example.com)
[Lien interne](posts/001-premiers-pas.fr.md)
[Lien interne dans un nouvel onglet](tab:posts/001-premiers-pas.fr.md)
```

<http://www.example.com>

[Ouvrir dans le même onglet](http://www.example.com)

[Ouvrir dans un nouvel onglet](tab:http://www.example.com)

[Lien interne](posts/001-premiers-pas.fr.md)

[Lien interne dans un nouvel onglet](tab:posts/001-premiers-pas.fr.md)

Si un lien interne est utilisé dans un texte mais n'existe pas, un avertissement est indiqué lors du build du blog.

# Images

L'intégration d'images dans le texte repose sur le standard Markdown. Les images peuvent être internes ou externes.

```
![Exemple d'image externe](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Exemple d'image interne](assets/img/got_wallpaper.jpg)
```

![Exemple d'image externe](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Exemple d'image interne](assets/img/got_wallpaper.jpg)

Par défaut, les images sont affichées pour ne pas dépasser la taille du texte en largeur et sont toujours centrées sur le texte. Ceci permet de s'assurer que les images trop grandes s'affichent correctement, y compris sur les écrans de smartphones.

Si une image interne est utilisée dans un texte mais n'existe pas, un avertissement est indiqué lors du build du blog.

# Modifier le design de Pureblog (avancé)

La configuration de votre Pureblog repose sur le fichier de configuration. Par défaut, le fichier de configuration se trouve dans `config/config.yml`. Ce fichier de configuration contient une section `theme` qui mentionne deux fichiers. Ces fichiers permettent d'adapter le design de votre Pureblog.

Le fichier de template (`theme.template_file`) est un fichier HTML qui définit la structure générale d'une page Pureblog. Vous pouvez l'adapter pour changer la structure générale d'une page.

Le fichier de template contient des paramètres qui sont remplacés lors de la construction du site. Les paramètres disponibles dans le template sont les suivants :

- `$lang` : le code langue de la page en cours.
- `$description` : le résumé de la page tel qu'il est décrit dans le header d'un blog post (sous `excerpt`).
- `$root` : le chemin relatif à la racine de construction de la page en cours (exemple : `..` pour une page principale pour une langue, `../..` pour une page de blog post). Ce paramètre est utilisé comme préfixe pour les URLs afin que l'affichage se passe bien.
- `$site_title` : le titre du site web tel que défini dans la configuration (`general.site_title`).
- `$title` : le titre de la page tel que défini dans le header d'un blog post (sous `title`).
- `$lang_switcher` : le bloc permettant de changer de langue sur une page.
- `$content` : le contenu rendu en HTML.
- `$author` : l'auteur tel que défini dans la configuration (`general.author`). Il est affiché dans le pied de page sous la forme `© {auteur} {année}`.
- `$year` : l'année du dernier build du site web.

Les modifications de style graphique peuvent être réalisées dans la feuille de style. Le fichier de style (`theme.style_file`) est un CSS qui définit les règles de formatage des différents éléments du site.

## Favicon à partir d'un emoji

Le favicon est la petite icône affichée dans les onglets du navigateur, les favoris et les résultats de recherche à côté du nom de votre site. Pureblog le génère automatiquement à partir d'un seul emoji défini dans `config/config.yml` :

```yaml
theme:
  favicon_emoji: "🤍"
```

Remplacez l'emoji par le caractère de votre choix — un cœur, un appareil photo, une fusée — pour donner à votre blog une identité distinctive. La modification prend effet lors du prochain build.

**Pourquoi un emoji plutôt qu'un fichier PNG ou ICO ?**

Les favicons traditionnels nécessitent des outils de retouche d'image dédiés, plusieurs résolutions (16×16, 32×32, 180×180…) et plusieurs kilo-octets de fichiers. Pureblog adopte une approche plus simple :

- **Aucun outil requis.** Un emoji est simplement un caractère texte : modifiez la configuration, relancez le build, c'est fait.
- **Format vectoriel.** L'emoji est rendu en SVG, ce qui garantit une netteté parfaite quelle que soit la taille et la densité d'écran, y compris les affichages HiDPI / Retina.
- **Poids nul.** Le SVG généré ne représente que quelques centaines d'octets, contre des dizaines de kilo-octets pour un jeu d'icônes classique.
- **Personnalité immédiate.** Un seul caractère suffit pour rendre l'onglet inimitable.

Le fichier `favicon.svg` généré est placé à la racine du répertoire de build et référencé sur chaque page — y compris la page de redirection racine — via une balise `<link rel="icon">`. La référence utilise une URL absolue dérivée de `general.site_url`, afin que les lecteurs de flux comme Inoreader résolvent et affichent correctement l'icône. Tous les navigateurs modernes prennent en charge les favicons SVG.

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
