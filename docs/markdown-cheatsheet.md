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

## Paragraphs and line breaks

Blank lines separate paragraphs. A single newline inside a paragraph is
collapsed to a space, matching standard Markdown behaviour.
