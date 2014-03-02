import unittest
from unittest import TestCase
from  htl.hocr import HOCRParser
from htl import model


class MyTestCase(TestCase):
    def test_parsing(self):
        parser = HOCRParser(True)
        htl_doc = parser.feed(open('data/mr-grover1.hocr', 'r',
                                   encoding='utf-8').read())
        print(model.dumps(htl_doc))

    def test_parsing2(self):
        parser = HOCRParser(True)
        htl_doc = parser.feed(open('data/mr-grover2.hocr',
                                   'r', encoding='utf-8').read())
        print(model.dumps(htl_doc))

if __name__ == '__main__':
    unittest.main()
