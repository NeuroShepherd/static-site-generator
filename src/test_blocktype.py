import unittest
from blocktype import BlockType

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        self.assertEqual(BlockType.PARAGRAPH, BlockType("paragraph"))

    def test_block_to_block_type_heading(self):
        self.assertEqual(BlockType.HEADING, BlockType("heading"))

    def test_block_to_block_type_code(self):
        self.assertEqual(BlockType.CODE, BlockType("code"))

    def test_block_to_block_type_quote(self):
        self.assertEqual(BlockType.QUOTE, BlockType("quote"))

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(BlockType.UNORDERED_LIST, BlockType("unordered_list"))

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(BlockType.ORDERED_LIST, BlockType("ordered_list"))