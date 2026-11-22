# Problem to solve

I ran the PageSpeed Insights to estimate the performance of the pages on Google.

It appears than the loading of the Google fonts impact potentially the speed of load.

The main insight is:

`Render-blocking requests Est savings of 740 ms`
`Requests are blocking the page’s initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path. LCP FCP Unscored`

The insight is linked to the load of the Google Fonts (Lora family).

Improve this.