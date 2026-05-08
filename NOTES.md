# Notes

This is a human-readable note related to the project. Nothing fancy, just some thoughts and ideas that I would like to pursuit.

## Notes for myself

### About Bear Blog

- I love the concept of Bear Blog (https://bearblog.dev)
  - The Manifesto of Herman: https://herman.bearblog.dev/manifesto/
  - Each page as a kind of "like" button and the page Discover have the list of 20 most popular blog posts according to a disclaimed algorithm (see bearblog.dev/discover/)
  - Concept of favicon with a emoji is nice

The algorithm for the ranking on Discover page:

```
This page is ranked according to the following algorithm:
Score = log10(U) + (S / (B * 86,400))

Where,
U = Upvotes of a post
S = Seconds since Jan 1st, 2020
B = Buoyancy modifier (currently at 14)

--
B values is used to modify the effect of time on the score. A lower B causes posts to sink faster with time.
```

## Work in progress

## Known issues

## URLs

## Future plans

- TODO : Tester les flux RSS avec Inoreader
- Support only 1 language (hide language switcher)
- Setup a better "startup website" (WIP)
- What about the Google description for the index pages? (only posts have description)
- Add a link to the Pureblog website on each page (www.pureblog.dev)
- When we click on the "website title", it routes to the default language; even if we are on another language. It should route to the current language.

- Check if the H1 in the body is OK based on aHref site audit
- Ensure that the first language is the default language
- When landing on the homepage, switch to the most appropriate language depending on the brower preferences
- If the page is long (more than 1 scroll, add a "Back" link at the end of the article)

- Add integration testing and packaging in CI/CD
- It would be great to link to an anchor which is a heading in another page
- Add a check to ensure that all MD files in the posts/ are formatted correctly (I got an issue while building the startup website because the format was incorrect, space in the filename)
- Convert images to WebP format to improve speed of the website.
- Allow users to add their pureblog in a list that appears on the main website?
