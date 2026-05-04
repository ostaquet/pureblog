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

## Paragraphs and line breaks

Blank lines separate paragraphs. A single newline inside a paragraph is
collapsed to a space, matching standard Markdown behaviour.
