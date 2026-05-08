---
title: Multilingual management
date: 2026-05-02
excerpt: Multilingual integration is a key strength of Pureblog. Discover how Pureblog is different and how languages are handled to ensure the best user experience and the best SEO.
---

Pureblog is first and foremost a multilingual blog engine. It was created after many attempts with existing solutions (WordPress, Ghost, Bearblog, Drupal, Chirpy/Jekyll). With each attempt, multilingual handling felt more like a hack than something integrated into the engine. Hacks work visually for the visitor but negatively impact SEO and the user experience when used with an RSS feed.

## Home pages and indexes

The home pages of the different languages are differentiated by a URL extension. This makes it possible to keep one RSS feed per language so that visitors can read the posts of your Pureblog in their preferred language.

Typically, the Pureblog you are currently reading is available in several languages. There are therefore several URLs to access the indexes:

- <https://www.pureblog.dev/en>
- <https://www.pureblog.dev/fr>
- <https://www.pureblog.dev/nl>
- ...

The available languages are defined in the `config/config.yml` configuration file under the `languages.codes` parameter. The first declared language is always the default language.

The default language is used to redirect from the base URL of your Pureblog. For this Pureblog, the default language is `en` (English). So a visitor opening the URL <https://www.pureblog.dev> is automatically redirected to <https://www.pureblog.dev/en>.

Every page of your Pureblog contains a language switcher, including the home pages. This switcher lets the visitor quickly switch to the language of their choice.

## RSS feeds and the sitemap

Each language has its own RSS feed. This allows visitors to follow the posts of your Pureblog in their favourite language. RSS feeds are always attached under a language URL, of the form <https://www.pureblog.dev/fr/feed.xml>.

The sitemap is unique for the entire site. It contains the home pages and the posts. For each page, the sitemap mentions the language and the alternative languages available for that page along with the URLs. This is often where other blog engines fall short, because they do not handle alternate links between posts in the sitemap.

To learn more about RSS feeds and sitemaps, see [the page on online visibility](posts/006-online-visibility.en.md).

## Links between languages for the same post

To improve SEO, a post can have a different URL depending on the language. This is also a difference compared to traditional blog engines.

The URL is always built from the post filename. The filename has the form `<id>-<slug>.<lang>.md`. The `id` identifier links together the same page written in different languages. The `slug` is the URL that will be used. The language is the 2-character ISO code (`lang`). So a file named `002-write-new-post.en.md` will be served at the URL `/en/write-new-post/`.

A post written in multiple languages can have URLs that differ per language. For example:

- `002-write-new-post.en.md` for English.
- `002-ecrire-nouvel-article.fr.md` for French.
- `002-schrijf-nieuw-bericht.nl.md` for Dutch.
- ...

The identifier acts as the connector between the different languages of the same post (in the example, the identifier is `002`).

As mentioned above, every page of your Pureblog contains a language switcher. This switcher is clearly visible to allow the visitor to read the post in another language. If the post is not available in a language, the switcher shows the language code with a strikethrough (e.g. ~~NL~~ ). If the visitor still clicks the strikethrough link, they are redirected to the current page.

When a post exists in one language but not in the others, a warning is shown during site generation.

## Language configuration

The available languages are listed in the `config/config.yml` configuration file in the `languages` section. This section contains a set of parameters allowing you to fine-tune the language configuration.

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

The language codes are listed under the `languages.codes` parameter. Language codes use [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (2-letter language codes).

The first language code is the default language of your Pureblog.

The `languages.reading_time_labels` and `languages.back_labels` parameters are the labels used during site generation to indicate the reading time of a post and the back-to-home label.

## What happens if a post exists in only one language?

The home pages, the sitemap and the RSS feeds rely exclusively on the presence of post files. So, if a file does not exist (the NL version, for example), the post does not appear anywhere on your Pureblog.

If the post is not available in a language, the language switcher shows the language code with a strikethrough (e.g. ~~NL~~ ). If the visitor clicks the strikethrough link anyway, they are redirected to the current page.

When a post exists in one language but not in the others, a warning is shown during site generation.

## Does Pureblog work with a single language?

Yes, Pureblog can be used with a single language. In that case, simply list a single language code in the configuration file (`languages.codes`).

Note that the redirection behaviour stays the same. If you only use the language code `en`, the home page `https://www.example.com` will still redirect to `https://www.example.com/en`. This makes it possible to add languages later and to start with a single-language Pureblog.

When only one language is configured, the language switcher is not displayed on home pages and post pages. In keeping with the minimalist spirit, there is no point cluttering the page with a switcher that has become useless.
