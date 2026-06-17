---
title: Design, layout and typography
date: 2026-05-03
excerpt: Some examples of typography, images and links; as well as the key files to adapt the design to your taste.
---

Pureblog is built around a minimalist design that covers the needs of publishing blog posts.

# Typography examples

## Headings and section titles

```
# Heading level 1
## Heading level 2
### Heading level 3
#### Heading level 4
```

# Heading level 1

## Heading level 2

### Heading level 3

#### Heading level 4

## Paragraphs and formatting

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar urna erat, et sollicitudin mi sodales id. Quisque sit amet egestas ex. Proin id diam ante. Duis varius porttitor luctus. Maecenas tempus nunc sed enim vehicula, sit amet laoreet turpis eleifend. Nunc vel sollicitudin neque. Quisque at laoreet metus. Proin sed odio nec urna eleifend interdum. Integer luctus magna nec neque consequat sagittis.
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar urna erat, et sollicitudin mi sodales id. Quisque sit amet egestas ex. Proin id diam ante. Duis varius porttitor luctus. Maecenas tempus nunc sed enim vehicula, sit amet laoreet turpis eleifend. Nunc vel sollicitudin neque. Quisque at laoreet metus. Proin sed odio nec urna eleifend interdum. Integer luctus magna nec neque consequat sagittis.

```
**Bold text**
_Italic text_
*Italic text*
~~Strikethrough text~~
`Inline code`
> Quote
```

**Bold text**

_Italic text_

_Italic text_

~~Strikethrough text~~

`Inline code`

> Quote

Empty lines separate paragraphs. A simple line break inside a paragraph is converted to a space, in line with the standard Markdown behaviour.

Note: strikethrough (`~~…~~`) is intentionally ignored inside inline code (between single backticks) and code blocks (between triple backticks), so that code samples are rendered as-is.

## Bullet lists

```
- First item
- Second item
- Third item
```

- First item
- Second item
- Third item

## Numbered lists

```
1. First item
2. Second item
3. Third item
```

1. First item
2. Second item
3. Third item

## Code

Inline code embedded in text:

```
`Inline code`
```

`Inline code`

Multiple lines of code:

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

There is no automatic line wrapping when laying out multiple lines of code.

# Link examples

There are 4 types of links:

- Automatic links (`<http://www.example.com>`)
- External links in the same tab (`[Open in the same tab](http://www.example.com)`)
- External links in a new tab (`[Open in a new tab](tab:http://www.example.com)`)
- Internal links in the same tab (`[Internal link](posts/001-getting-started.en.md)`)

The `tab:` prefix and internal links can be combined. For example, `[Internal link in a new tab](tab:posts/001-getting-started.en.md)` opens the resolved internal link in a new tab.

🔐 Security note: links opened in a new tab (`tab:`) automatically receive the attributes `target="_blank"` and `rel="noopener noreferrer"`, which protects your visitors from _tabnabbing_.

```
<http://www.example.com>
[Open in the same tab](http://www.example.com)
[Open in a new tab](tab:http://www.example.com)
[Internal link](posts/001-getting-started.en.md)
[Internal link in a new tab](tab:posts/001-getting-started.en.md)
```

<http://www.example.com>

[Open in the same tab](http://www.example.com)

[Open in a new tab](tab:http://www.example.com)

[Internal link](posts/001-getting-started.en.md)

[Internal link in a new tab](tab:posts/001-getting-started.en.md)

If an internal link is used in text but does not exist, a warning is reported during the blog build.

# Images

Embedding images in text relies on the standard Markdown syntax. Images can be internal or external.

```
![External image example](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Internal image example](assets/img/got_wallpaper.jpg)
```

![External image example](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Internal image example](assets/img/got_wallpaper.jpg)

By default, images are displayed so as not to exceed the width of the text and are always centred. This ensures that overly large images render properly, including on smartphone screens.

If an internal image is used in text but does not exist, a warning is reported during the blog build.

# Customising the design of Pureblog (advanced)

The configuration of your Pureblog relies on the configuration file. By default, the configuration file is at `config/config.yml`. This configuration file contains a `theme` section that references two files. These files allow you to adapt the design of your Pureblog.

The template file (`theme.template_file`) is an HTML file that defines the overall structure of a Pureblog page. You can adapt it to change the overall page structure.

The template file contains parameters that are replaced when the site is built. The parameters available in the template are:

- `$lang`: the language code of the current page.
- `$description`: the page summary as described in the front matter of a blog post (`excerpt`).
- `$root`: the relative path to the build root from the current page (e.g. `..` for a language home page, `../..` for a blog post page). This parameter is used as a prefix for URLs to ensure rendering works correctly.
- `$site_title`: the site title as defined in the configuration (`general.site_title`).
- `$title`: the page title as defined in the front matter of a blog post (`title`).
- `$lang_switcher`: the block that lets the visitor switch language on a page.
- `$content`: the content rendered as HTML.
- `$author`: the author as defined in the configuration (`general.author`). It is shown in the footer as `© {author} {year}`.
- `$year`: the year of the latest build of the website.

Visual style changes can be made in the stylesheet. The style file (`theme.style_file`) is a CSS file that defines the formatting rules for the various elements of the site.

## Favicon from an emoji

The favicon is the small icon displayed in browser tabs, bookmarks, and search results next to your site name. Pureblog generates it automatically from a single emoji set in `config/config.yml`:

```yaml
theme:
  favicon_emoji: "🤍"
```

Change the emoji to any character you like — a heart, a camera, a rocket — to give your blog a distinctive identity. The change takes effect on the next build.

**Why an emoji instead of a PNG or ICO file?**

Traditional favicons require dedicated image editing tools, multiple resolutions (16×16, 32×32, 180×180…) and several kilobytes of files. Pureblog takes a simpler path:

- **No tooling needed.** An emoji is just a text character: edit the config, rebuild, done.
- **Vector format.** The emoji is rendered as an SVG, so it is perfectly sharp at any size and on any screen density, including HiDPI / Retina displays.
- **Zero weight.** The generated SVG is a few hundred bytes, compared with tens of kilobytes for a typical icon set.
- **Instant personality.** One character is enough to make the tab unmistakably yours.

The generated `favicon.svg` is placed at the root of the build directory and referenced from every page via a `<link rel="icon">` tag. Any modern browser supports SVG favicons.

## Custom 404 page

When a visitor lands on a URL that does not exist on your site, they see a 404 error. By default, hosting providers show a plain, unstyled error page. Pureblog automatically generates a styled `404.html` at the root of the site that matches your blog's visual identity, so the visitor stays in a consistent environment and can find their way back to the homepage.

The page is entirely self-contained: the stylesheet is embedded directly in the HTML and all links use the absolute URL configured in `general.site_url`. This ensures that styles and navigation work correctly regardless of the URL depth at which the hosting provider serves the error page (for example, Firebase serves the same `404.html` whether the missing URL is `/brol` or `/en/brol`).

The page displays the "page not found" message in the default language with a link to the homepage. Both texts are configured in `config/config.yml` under the `languages` section:

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

A language switcher is also included, linking directly to the index of each configured language so visitors can navigate even after landing on a missing URL.

On Firebase Hosting, the `404.html` file at the root is served automatically for any unmatched URL. Other static hosting providers (Netlify, GitHub Pages, etc.) follow the same convention.
