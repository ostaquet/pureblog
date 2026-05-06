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

- Setup a better "startup website".
- Add a link to the Pureblog website on each page (www.pureblog.dev)
- Add integration testing and packaging in CI/CD
- Support only 1 language (hide language switcher)
- Convert images to WebP format to improve speed of the website.
- Ensure that the first language is the default language
- When landing on the homepage, switch to the most appropriate language depending on the brower preferences
- Allow users to add their pureblog in a list that appears on the main website?
