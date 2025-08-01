import unittest

from nodes.textnode import TextNode,TextType
from markdownparser import split_nodes_delimiter,extract_markdown_images,extract_markdown_links, split_nodes_image, split_nodes_links, text_to_textnodes,markdown_to_blocks,BlockType,block_to_block_type, markdown_to_html_node

class TestMarkdownParter(unittest.TestCase):

    def test_split_nodes_delimiter_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])


    def test_split_nodes_delimiter_single(self):
        node = TextNode("Bold of you to come here", TextType.BOLD)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node3 = TextNode("print(this works)", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3])
        self.assertListEqual(new_nodes, [
        TextNode("Bold of you to come here", TextType.BOLD),
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        TextNode("print(this works)", TextType.CODE)
        ])

    def test_split_nodes_delimiter_single_normal_text(self):
        node = TextNode("Bold of you to come here", TextType.BOLD)
        node2 = TextNode("This is text with no code block word", TextType.TEXT)
        node3 = TextNode("print(this works)", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2, node3])
        self.assertListEqual(new_nodes, [
        TextNode("Bold of you to come here", TextType.BOLD),
        TextNode("This is text with no code block word", TextType.TEXT),
        TextNode("print(this works)", TextType.CODE)
        ])


    def test_split_nodes_delimiter_multiple_simple(self):
        node = TextNode("This is a **bold text** with some `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(new_nodes, [
        TextNode("This is a ", TextType.TEXT),
        TextNode("bold text", TextType.BOLD),
        TextNode(" with some ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_overlap(self):
        node = TextNode("This is a **bold _text** with_ some `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(new_nodes, [
        TextNode("This is a ", TextType.TEXT),
        TextNode("bold ", TextType.BOLD),
        TextNode("text", TextType.BOLD),
        TextNode("text", TextType.ITALIC),
        TextNode(" with", TextType.ITALIC),
        TextNode(" some ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_improper_amount_of_delims(self):
        node = TextNode("This is a **bold _text** with some `code block` wo`rd", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(new_nodes, [
        TextNode("This is a ", TextType.TEXT),
        TextNode("bold _text", TextType.BOLD),
        TextNode(" with some ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" wo`rd", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_same_delims(self):
        node = TextNode("This **is a **bold text** with some **`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(new_nodes, [
        TextNode("This ", TextType.TEXT),
        TextNode("is a ", TextType.BOLD),
        TextNode("bold text", TextType.TEXT),
        TextNode(" with some ", TextType.BOLD),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_same_delims_next_to_each_other_without_text_inside(self):
        node = TextNode("This is a ****bold text** with some `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node])
        self.assertListEqual(new_nodes, [
        TextNode("This is a ", TextType.TEXT),
        TextNode("bold text** with some ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_images_no_links_recognized(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![image](https://i.i554mgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image", "https://i.i554mgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_empty_alt_or_url(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![](https://i.imgur.com/zjjcJKZ.png) ![image]()"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_same_type_brackets_inside(self):
        matches = extract_markdown_images(
        "This is text with an ![()image]([]https://i.imgur.com/zjjcJKZ.png) ![j[gfgf]](https://i.imgur.com/zjjcJKZ.png) ![image](hjhjh7())"
        )
        self.assertListEqual([("()image", "[]https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![image](https://i.i554mgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image", "https://i.i554mgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_not_properly_closed_brackets(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![image(https://i.i554mgur.com/zjjcJKZ.png) !image]https://i.i554mgur.com/zjjcJKZ.png ![image]https://i.i554mgur.com/zjjcJKZ.png) !image(https://i.i554mgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://bootdev.com) ![image](https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([("link", "https://bootdev.com")], matches)

    def test_extract_markdown_links_multiple_links_no_image_recognized(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://bootdev.com) ![image](https://i.imgur.com/zjjcJKZ.png [link2](https://bootdev2.com)"
        )
        self.assertListEqual([("link", "https://bootdev.com"),("link2", "https://bootdev2.com")], matches)

    def test_extract_markdown_links_empty_alt_or_url(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://bootdev.com) [](https://i.imgur.com/zjjcJKZ.png) [link2]()"
        )
        self.assertListEqual([("link", "https://bootdev.com")], matches)

    def test_extract_markdown_links_no_same_type_brackets_inside(self):
        matches = extract_markdown_links(
        "This is text with an [link()]([]https://bootdev.com) [bbjb[]](https://i.imgur.com/zjjcJKZ.png) [link2](KN()KN)"
        )
        self.assertListEqual([("link()", "[]https://bootdev.com")], matches)

    def test_extract_markdown_links_not_properly_closed_brackets(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://bootdev.com) [bbjb(https://i.imgur.com/zjjcJKZ.png)] [link2(KNKN) [link3]KNKN) [link4]KNKN"
        )
        self.assertListEqual([("link", "https://bootdev.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode("Some ![image](url.com) here.", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.com"),
                TextNode(" here.", TextType.TEXT),
            ],
            result,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "![img1](url1.com) mid text ![img2](url2.com) end.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1.com"),
                TextNode(" mid text ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.com"),
                TextNode(" end.", TextType.TEXT),
            ],
            result,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is just plain text with no images.", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_images_malformed_image(self):
        node = TextNode("This is not an image: ![alt](broken", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_images_nested_image_like_text(self):
        node = TextNode("Look at this: ![alt[inner]](url.com)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_images_ends_with_image(self):
        node = TextNode("text before ![alt](url.com)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.com"),
            ],
            result,
        )

    def test_split_links_single(self):
        node = TextNode("Here is a [link](https://example.com) in text.", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in text.", TextType.TEXT),
            ],
            result,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Start [one](url1) mid [two](url2) end.",
            TextType.TEXT,
        )
        result = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("one", TextType.LINK, "url1"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("two", TextType.LINK, "url2"),
                TextNode(" end.", TextType.TEXT),
            ],
            result,
        )

    def test_split_links_no_links(self):
        node = TextNode("Nothing linky here!", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertListEqual([node], result)

    def test_split_links_malformed(self):
        node = TextNode("[Broken](link.com", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertListEqual([node], result)

    def test_split_links_ends_with_link(self):
        node = TextNode("Click this [now](url.com)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Click this ", TextType.TEXT),
                TextNode("now", TextType.LINK, "url.com"),
            ],
            result,
        )

    def test_split_links_ignores_images(self):
        node = TextNode("![img](img.com) and [link](url.com)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("![img](img.com) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            result,
        )

    def test_split_links_broken_nested_brackets(self):
        node = TextNode("[broken[link]](url.com)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertListEqual([node], result)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],textnodes)

    def test_text_to_textnodes_plain_text(self):
        text = "Just a simple sentence with no markdown."
        textnodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just a simple sentence with no markdown.", TextType.TEXT)], textnodes)

    def test_text_to_textnodes_mixed_styles(self):
        text = "Some _italic_ and **bold** and [a link](https://example.com)."
        textnodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ], textnodes)

    def test_text_to_textnodes_malformed_markdown(self):
        text = "Text with a broken ![image]( and a broken [link(too)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("Text with a broken ![image]( and a broken [link(too)", TextType.TEXT),
        ], textnodes)

    def test_text_to_textnodes_image_link_together(self):
        text = "![img](http://img.com) [link](http://link.com)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("img", TextType.IMAGE, "http://img.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://link.com"),
        ], textnodes)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Paragraph one.",
            "Paragraph two.",
            "Paragraph three."
        ])

    def test_markdown_to_blocks_strip_whitespace_lines(self):
        md = "   Paragraph one.   \n\n   Paragraph two.\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Paragraph one.",
            "Paragraph two."
        ])

    def test_markdown_to_blocks_preserve_multiline_blocks(self):
        md = "Line 1\nLine 2\n\nLine 3\nLine 4"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Line 1\nLine 2",
            "Line 3\nLine 4"
        ])

    def test_block_to_block_type_heading_levels(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("Paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Paragraph"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        code_block = "```\ndef func():\n    pass\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type_quote_block(self):
        block = "> This is a quote\n> It has multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list_valid(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_invalid_numbering(self):
        block = "1. First\n2. Second\n4. Wrong"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_mixed_content(self):
        block = "This is a regular paragraph with **bold** and _italic_."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_unordered(self):
        block = "- Item 1\n• Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_empty_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block_inline_ticks(self):
        block = "```This is not a block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_unordered_list_with_extra_indent(self):
        block = "- Item 1\n   - Subitem"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        markdown = "This is a simple paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].children[0].value, "This is a simple paragraph.")

    def test_heading_level_1(self):
        markdown = "# Heading One"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[0].children[0].value, "Heading One")

    def test_heading_level_3(self):
        markdown = "### Third Level Heading"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "h3")
        self.assertEqual(node.children[0].children[0].value, "Third Level Heading")

    def test_inline_code_block(self):
        markdown = "```This is not a block```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertIn("This is not a block", node.children[0].children[0].value)

    def test_code_block_multiline(self):
        markdown = "```\nline 1\nline 2\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertIn("line 1", node.children[0].children[0].value)
        self.assertIn("line 2", node.children[0].children[0].value)

    def test_blockquote(self):
        markdown = "> This is a quote"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "blockquote")
        self.assertEqual(node.children[0].children[0].value.strip(), "This is a quote")

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        node = markdown_to_html_node(markdown)
        print(node.to_html())
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].children[0].value, "Item 1")

    # def test_ordered_list(self):
    #     markdown = "1. First item\n2. Second item"
    #     node = markdown_to_html_node(markdown)
    #     self.assertEqual(node.children[0].tag, "ol")
    #     self.assertEqual(len(node.children[0].children), 2)
    #     self.assertEqual(node.children[0].children[1].children[0].value, "Second item")

    # def test_mixed_blocks(self):
    #     markdown = "# Title\n\nSome paragraph text.\n\n- List item"
    #     node = markdown_to_html_node(markdown)
    #     tags = [child.tag for child in node.children]
    #     self.assertEqual(tags, ["h1", "p", "ul"])

    # def test_empty_markdown(self):
    #     markdown = ""
    #     node = markdown_to_html_node(markdown)
    #     self.assertEqual(node.tag, "div")
    #     self.assertEqual(node.children, [])

    # def test_heading_without_space_is_paragraph(self):
    #     markdown = "##Heading with no space"
    #     node = markdown_to_html_node(markdown)
    #     self.assertEqual(node.children[0].tag, "p")
    #     self.assertEqual(node.children[0].children[0].value.strip(), "##Heading with no space")

if __name__ == "__main__":
    unittest.main()