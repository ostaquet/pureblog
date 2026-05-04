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

- Convert image to web image format to improve speed of the website.
- Setup a better "starting website".
