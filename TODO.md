# TO-DO
- Make it so textnode.split_nodes_image() and split_nodes_link() do not cross. (E.g. a line with an image should not be parsed by split_nodes_link().)
- Fix the multiple images (and probably multiple links) bug. (I suspect this is caused because I do not update the indices for found_images etc. properly.)
- Regarding the first issue: there is probably an issue with a sentence with both a link and an image as well.

