# Pureblog Markdown cheatsheet

Pureblog renders blog post bodies through `src/markdown_parser.py`. The
following syntax is supported. Anything not listed here is either
unsupported or untested — feel free to extend the parser (and this
document) when you need more.

## Headers

```markdown
# Header 1
## Header 2
### Header 3
#### Header 4
```

Renders as `<h1>` … `<h4>`.

## Emphasis

| Markdown        | HTML                          |
| --------------- | ----------------------------- |
| `**bold**`      | `<strong>bold</strong>`       |
| `_italic_`      | `<em>italic</em>`             |
| `*italic*`      | `<em>italic</em>`             |
| `~~strike~~`    | `<del>strike</del>`           |

Strikethrough is intentionally ignored inside inline code (`` `~~x~~` ``)
and fenced code blocks so that source snippets stay verbatim.

## Lists

Unordered list — start lines with `-`:

```markdown
- first
- second
- third
```

Ordered list — start lines with `1.`, `2.`, … :

```markdown
1. first
2. second
3. third
```

## Blockquotes

```markdown
> A wise quote.
> Continues on the next line.
```

Renders inside `<blockquote>`.

## Code

Inline code with single backticks:

```markdown
Use the `make build` command.
```

Fenced code blocks with triple backticks (optionally followed by a
language hint, used as a CSS class):

````markdown
```python
def hello() -> str:
    return "world"
```
````

Renders as `<pre><code>…</code></pre>`.

## Images

External images use the standard Markdown syntax with an absolute URL:

```markdown
![External image example](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)
```

Internal images live under the configured `general.assets_dir`
(default: `assets/`). The whole directory is copied verbatim into
`build/assets/` at build time, so reference assets relative to the
project root:

```markdown
![Internal image example](assets/img/documentation.png)
```

The build rewrites relative `<img src="...">` URLs to be relative to
the page's root, so the same Markdown works on both index and post
pages. If a referenced internal image cannot be found in `assets_dir`,
the build prints a warning to stderr but still succeeds.

## Links

Pureblog renders four kinds of links:

```markdown
<http://www.example.com>

[Open in same tab](http://www.example.com)

[Open in new tab](tab:http://www.example.com)

[Internal link](posts/001-bonjour-monde.fr.md)
```

- Auto-links (`<URL>`) and standard inline links (`[text](URL)`) render as
  plain `<a href="URL">…</a>` and open in the same tab.
- A `tab:` prefix on the URL opens the link in a new tab. The prefix is
  stripped at build time and `target="_blank" rel="noopener noreferrer"`
  is added to the anchor (the `rel` value protects against tabnabbing).
- Internal links use the source filename of the target post under the
  configured `general.posts_dir` (default: `posts/`). The path is
  rewritten to the deployed URL `/{lang}/{slug}/`. If the referenced
  source file does not exist, the build prints a warning to stderr but
  still renders the link.

`tab:` and internal-link rewrites compose: `[x](tab:posts/001-foo.en.md)`
opens the resolved internal URL in a new tab.

## Paragraphs and line breaks

Blank lines separate paragraphs. A single newline inside a paragraph is
collapsed to a space, matching standard Markdown behaviour.
