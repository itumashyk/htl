import unittest
from unittest import TestCase
from  htl.hocr import HOCRParser


class MyTestCase(TestCase):
    def test_parsing(self):
        parser = HOCRParser()
        parser.feed(open('data/mr-grover1.hocr', 'r', encoding='utf-8').read())


if __name__ == '__main__':
    unittest.main()
