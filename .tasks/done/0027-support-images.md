# Problem to solve

Blog post could contains pictures inside the text.

The pictures are added throught the classic Markdown directive.

Example:

![External image example](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)

![Internal image example](assets/img/documentation.png)

It is important that all assets in `assets/*` are copied into `build/` for proper deployment.

If the internal image is not available, output a warning during build process.

Also, update the `docs/markdown-cheatsheet.md`.
