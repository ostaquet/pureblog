# Problem to solve

Each post has normally a translation in the different languages.

Example with article `001` composed by `posts/001-bonjour-monde.fr.md`, `posts/001-dag-wereld.nl.md` and `posts/001-hello-world.en.md`.

However, the user may forget to put all the different translations in the `posts/` folder.

When the build is performed (with `src/build.py`), the program should output a warning when there is a missing translation for an article. This is not a blocking warning and the blog should be available.

Additionally to the warning, the links to the translation should be managed to avoid an ugly 404 error page. For the not translated post, the language switcher should be strikethrough if the translation is not available for this specific post. When the user clicks on the strikethrough link, the link directs to the current page.

Example with page `posts/002-other-post.en.md`:

- The post is available on http://localhost:8000/en/other-post/.
- This post has no translations in fr and nl.
- On the top of the page, the language selector is `en | fr | nl`.
- As there is no fr and nl translations, the `fr` and `nl` links are strikethrough and link to http://localhost:8000/en/other-post/
