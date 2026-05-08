---
title: Writing a new blog post
date: 2026-05-04
excerpt: This tutorial will guide you through writing a post on your Pureblog, and it is worth reading even if you have used other blog engines before.
---

This tutorial will guide you through writing a post on your Pureblog.

## Naming convention and folders

By default, the posts of your Pureblog live in the `posts/` folder.

Create a new file named `<id>-<slug>.<lang>.md`. For example: `042-first-post.en.md`.

## Front matter

Your post starts with a header that helps with SEO and the structure of your site. Fill the front matter with the lines below:

```
---
title: My first post
date: 2026-05-07
---
```

## Publication date

For simplicity, Pureblog only uses the date for posts. Since RSS feeds also require time and timezone, those are configured in the configuration file (`publish` section). The default timezone is `Europe/Brussels` (configurable via `publish.default_timezone`) and daylight saving time is handled automatically.

## Post description

By default, the first 200 characters of the post are used as the description on the home page, in the RSS feed and in the SEO meta tags. If you wish to set the description manually, you can customise it with the `excerpt` tag in the front matter.

For example:

```
---
title: My first post
date: 2026-05-07
excerpt: This is my first post on Pureblog
---
```

## Content

After the front matter, you are free to write whatever content you want. The layout and the various typography options are described on the [page about design](posts/004-design-layout-and-typography.en.md).

## Reading time

Pureblog automatically computes an estimated reading time for each post (at 200 words per minute, with a minimum of one minute). This time is shown next to the date, both on the home page and on the post page. The associated label (e.g. "min read" in English) is configured per language in `languages.reading_time_labels` of the configuration file.

## Writing the post in other languages

You can now write your post in other languages such as French and Dutch. The only rule to follow is that the identifier must be identical.

So you can create the posts `042-premier-article.fr.md` and `042-eerst-bericht.nl.md`. They will be automatically linked to your first post as translations.

You will find more [details about multilingual handling on the dedicated page](posts/005-multilingual-management.en.md).
