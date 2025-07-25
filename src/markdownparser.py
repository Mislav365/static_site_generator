from config import DELIMITERS
from nodes.textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        events = _parse_styled_spans(_find_delimiters_in_text(node.text, DELIMITERS.keys()))
        active_styles = []
        last_pos = 0

        for pos, delim, kind in events:
            if pos > last_pos:
                span_text = node.text[last_pos:pos]
                if not active_styles:
                    new_nodes.append(TextNode(span_text, TextType.TEXT))
                else:
                    for style in active_styles:
                        new_nodes.append(TextNode(span_text, style))

            style = DELIMITERS[delim]
            if kind == 'open':
                active_styles.append(style)
            elif kind == 'close':
                if style in active_styles:
                    active_styles.remove(style)

            last_pos = pos + len(delim)

        if last_pos < len(node.text):
            span_text = node.text[last_pos:]
            if not active_styles:
                new_nodes.append(TextNode(span_text, TextType.TEXT))
            else:
                for style in active_styles:
                    new_nodes.append(TextNode(span_text, style))

    return new_nodes


def _parse_styled_spans(indexes):
    events = []
    for delim, positions in indexes.items():
        for i, pos in enumerate(positions):
            kind = 'open' if i % 2 == 0 else 'close'
            events.append((pos, delim, kind))

    events.sort()
    return events


def _find_delimiters_in_text(text, delimiters):
    indexes = {d: [] for d in delimiters}
    i = 0
    while i < len(text):
        matched = False
        for d in sorted(delimiters, key=len, reverse=True):  # longest first
            if text[i:i+len(d)] == d:
                indexes[d].append(i)
                i += len(d)
                matched = True
                break
        if not matched:
            i += 1

    for d in indexes:
        if len(indexes[d]) % 2 == 1:
            indexes[d].pop()
    return indexes