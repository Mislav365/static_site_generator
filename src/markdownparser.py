from config import DELIMITERS
from nodes.textnode import TextType, TextNode
import re

# params = list filled with nodes.TextType
# return = list of updated nodes in which every TextNode of TextType.TEXT was properly split if it contained properly placed delimiters mentioned in config.py
def split_nodes_delimiter(old_nodes):
    new_nodes = []

    # we iterate over each node in old_nodes
    for node in old_nodes:
        # every node besides type TEXT is already processed, so we just append it to new_nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # we call private func _find_delimiters_in_text to find all delimiter positions in node.text
        # then we call _parse_styled_spans to convert them into (position, delimiter, kind) tuples
        events = _parse_styled_spans(_find_delimiters_in_text(node.text, DELIMITERS.keys()))

        active_styles = []  # keeps track of currently open styles
        last_pos = 0  # last processed character index

        # we iterate over each (position, delimiter, kind) in sorted order
        for pos, delim, kind in events:
            # if there's any text between last_pos and current position, we create a TextNode for it
            if pos > last_pos:
                span_text = node.text[last_pos:pos]
                # if no styles are active, it's a plain TEXT node
                if not active_styles:
                    new_nodes.append(TextNode(span_text, TextType.TEXT))
                else:
                    # otherwise, apply all currently active styles to span_text
                    for style in active_styles:
                        new_nodes.append(TextNode(span_text, style))

            # we get the corresponding TextType style from the delimiter
            style = DELIMITERS[delim]

            # if delimiter is opening, we add the style to active_styles
            if kind == 'open':
                active_styles.append(style)
            # if it's closing, we remove it from active_styles if it exists
            elif kind == 'close':
                if style in active_styles:
                    active_styles.remove(style)

            # move last_pos forward past the delimiter
            last_pos = pos + len(delim)

        # after loop, if there's any remaining text after last_pos, we add it too
        if last_pos < len(node.text):
            span_text = node.text[last_pos:]
            # same style check as before
            if not active_styles:
                new_nodes.append(TextNode(span_text, TextType.TEXT))
            else:
                for style in active_styles:
                    new_nodes.append(TextNode(span_text, style))

    return new_nodes


# function that receives a dictionary of delimiter positions
# iterates over positions and adds a third element to each (delimiter, position) tuple that says whether it's an 'open' or 'close' delimiter
# params = dict -> keys = delimiter string, values = list of integer positions where delimiter appears
# return = list of tuples -> (int position, str delimiter, str kind)
def _parse_styled_spans(indexes):
    events = []

    # for each delimiter and its list of positions
    for delim, positions in indexes.items():
        # we loop through all positions and label them alternately as 'open' and 'close'
        for i, pos in enumerate(positions):
            kind = 'open' if i % 2 == 0 else 'close'
            events.append((pos, delim, kind))

    # sort all events by position in ascending order so we can process them correctly
    events.sort()
    return events


# function that finds all valid delimiter positions in the given text
# params = text = str, delimiters = iterable of delimiter strings
# return = dict -> keys = delimiter string, values = list of valid positions (even count only)
def _find_delimiters_in_text(text, delimiters):
    indexes = {d: [] for d in delimiters}
    i = 0

    # iterate over the text and try to match any delimiter at current position
    while i < len(text):
        matched = False
        # check for longest delimiters first to avoid partial matches (e.g., '**' before '*')
        for d in sorted(delimiters, key=len, reverse=True):
            if text[i:i+len(d)] == d:
                indexes[d].append(i)  # store the position of the match
                i += len(d)  # skip ahead by length of matched delimiter
                matched = True
                break
        if not matched:
            i += 1  # no match at this position, move forward by 1

    # make sure each delimiter has an even number of matches (open/close pairs only)
    for d in indexes:
        if len(indexes[d]) % 2 == 1:
            indexes[d].pop()  # remove last unmatched delimiter

    return indexes


# function that finds all markdown image patterns in given text
# markdown image syntax is: ![alt text](image_url)
# params = text = str
# return = list of tuples (alt_text, url)
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]+)\]\(([^\(\)]+)\)", text)


# function that finds all markdown link patterns in given text
# markdown link syntax is: [link text](url)
# pattern ignores images (which start with '!')
# params = text = str
# return = list of tuples (link_text, url)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)


# params = list filled with nodes.TextType
# return = list of updated nodes in which every TextNode of TextType.TEXT was properly split if it contained previously decided upon form for images ![alt text](url)
def split_nodes_image(old_nodes):
    new_nodes = []

    # we iterate over each node in old_nodes
    for node in old_nodes:
        # every node besides type TEXT is already processed, so we just append it to new_nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_pos = 0

        # call the function expecting it to extract image matches
        images = extract_markdown_images(text)

        # iterate over each extracted image tuple (alt text, url)
        for image in images:
            to_find = f"![{image[0]}]({image[1]})"  # reconstruct the exact markdown substring

            # find the position of the image markdown substring inside the text
            start = text.find(to_find)
            if start == -1:
                continue
            end = start + len(to_find)

            # if there's plain text before the image, add it as a new node
            if start > last_pos:
                before_text = text[last_pos:start]
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            # add the image as a TextNode of type IMAGE
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            # update the last processed index
            last_pos = end

        # if there's remaining plain text after the last image, add it
        if last_pos < len(text):
            remaining = text[last_pos:]
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


# params = list filled with nodes.TextType
# return = list of updated nodes in which every TextNode of TextType.TEXT was properly split if it contained previously decided upon form for links [alt text](url)
def split_nodes_links(old_nodes):
    new_nodes = []

    # we iterate over each node in old_nodes
    for node in old_nodes:
        # every node besides type TEXT is already processed, so we just append it to new_nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_pos = 0

        # call the function expecting it to extract link matches
        links = extract_markdown_links(text)

        # iterate over each extracted link tuple (link text, url)
        for link in links:
            to_find = f"[{link[0]}]({link[1]})"  # reconstruct the exact markdown substring

            # find the position of the link markdown substring inside the text
            start = text.find(to_find)
            if start == -1:
                continue
            end = start + len(to_find)

            # if there's plain text before the link, add it as a new node
            if start > last_pos:
                before_text = text[last_pos:start]
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            # add the link as a TextNode of type LINK
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            # update the last processed index
            last_pos = end

        # if there's remaining plain text after the last link, add it
        if last_pos < len(text):
            remaining = text[last_pos:]
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_image(split_nodes_links(split_nodes_delimiter([node])))

