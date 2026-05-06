---
title: Design, mise en page et typographie
date: 2026-05-03
excerpt: Quelques exemples de typographie, images et liens; ainsi que les fichiers clés pour adapter le design à votre gôut.
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

Il existe 5 types de liens :

- Les liens automatiques (`<http://www.example.com>`)
- Les liens externes dans le même onglet (`[Ouvrir dans le même onglet](http://www.example.com)`)
- Les liens externes dans un nouvel onglet (`[Ouvrir dans un nouvel onglet](tab:http://www.example.com)`)
- Les liens internes dans le même onglet (`[Lien interne](posts/001-qu-est-ce-que-pureblog.fr.md)`)
- Les liens internes dans un nouvel onglet (`[Lien interne dans un nouvel onglet](tab:posts/001-qu-est-ce-que-pureblog.fr.md)`)

```
<http://www.example.com>
[Ouvrir dans le même onglet](http://www.example.com)
[Ouvrir dans un nouvel onglet](tab:http://www.example.com)
[Lien interne](posts/001-qu-est-ce-que-pureblog.fr.md)
[Lien interne dans un nouvel onglet](tab:posts/001-qu-est-ce-que-pureblog.fr.md)
```

<http://www.example.com>

[Ouvrir dans le même onglet](http://www.example.com)

[Ouvrir dans un nouvel onglet](tab:http://www.example.com)

[Lien interne](posts/001-qu-est-ce-que-pureblog.fr.md)

[Lien interne dans un nouvel onglet](tab:posts/001-qu-est-ce-que-pureblog.fr.md)

Si un lien interne est utilisé dans un texte mais n'existe pas, un avertissement est indiqué lors du build du blog.

# Images

L'intégration d'images dans le texte repose sur le standard Markdown. Les images peuvent être internes ou externes.

```
![Exemple d'image externe](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Exemple d'image interne](assets/img/documentation.png)
```

![Exemple d'image externe](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Exemple d'image interne](assets/img/documentation.png)

Par défaut, les images sont affichées pour ne pas dépasser la taille du texte en largeur et sont toujours centrées sur le texte. Ceci permet de s'assurer que les images trop grande s'affichent correctement, y compris sur les écrans de smartphones.

Si une image interne est utilisé dans un texte mais n'existe pas, un avertissement est indiqué lors du build du blog.

# Modifier le design de Pureblog (avancé)

La configuration de votre Pureblog repose sur le fichier de configuration. Par défaut, le fichier de configuration se trouve dans `config/config.yml`. Ce fichier de configuration contient une section `theme` qui mentionne deux fichiers. Ces fichiers permettent d'adapter le design de votre Pureblog.

Le fichier de template (`theme.template_file`) est un fichier HTML qui définit la structure générale d'une page Pureblog. Vous pouvez l'adapter pour changer la structure générale d'une page.

Le fichier de template contient des paramètres qui sont remplacés lors de la construction du site. Les paramètres disponibles dans le template sont les suivants :

- `$lang` : le code langue de la page en cours.
- `$description` : le résumé de la page tel qu'il est décrit dans le header d'un blog post (sous `excerpt`).
- `$root` : le chemin relatif à la racine de constructuion de la page en cours (exemple : `..` pour une page principale pour une langue, `../..` pour un page de blog post). Ce paramètre est utilisé comme préfixe pour les URLs afin que l'affichage se passe bien.
- `$site_title` : le titre du site web tel que définit dans la configuration (`general.site_title`).
- `$title` : le titre de la page tel que définit dans le header d'un blog post (sous `title`).
- `$lang_switcher` : le blog permettant de changer de langue sur une page.
- `$content` : le contenu rendu en HTML.
- `$author` : l'auteur tel que définit dans la configuration (`general.author`).
- `$year` : l'année du dernier build du site web.

Les modifications de style graphique peuvent être réalisées dans la feuille de style. Le fichier de style (`theme.style_file`) est un CSS qui définit les règles de formatage des différents éléments du site.
