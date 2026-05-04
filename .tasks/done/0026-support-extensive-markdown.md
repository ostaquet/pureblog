# Problem to solve

In the current implementation, we have a limited support of the Markdown for the blog post.

I would like to support some layout in the Markdown. Such as:

- Emphasis
  - **bold**
  - _italic_
  - ~~strikethrough~~
  - # Header 1
  - ## Header 2
  - ### Header 3
  - #### Header 4
  - Generic list item
  - Number list item
  - > Quotes
  - Displaying code with `code`
  - Displaying multiple lines of code with `Multiple lines of code`

All Markdown layout available in Pureblog must be described in `docs/markdown-cheatsheet.md`.

The parsing of the Markdown posts into HTML should be in a specific Python file (to avoid having to much logic in the builder and to be tested easily).
