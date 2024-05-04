# TO-DO
- Currently calling split_nodes_images() on a sentence with an image and a link will return an empty list. Same in the inverse case. Not exactly desirable behaviour but better than the alternative for the time being where it will interpret the link as an image (due to how I coded split_nodes_delimiter()) or image as a link depending on the function called.
