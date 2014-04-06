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
        htl_doc = parser.feed(open('data/text-linux1.hocr',
                                   'r', encoding='utf-8').read())
        print(model.dumps(htl_doc))

    def test_parsing3(self):
        parser = HOCRParser(True)
        htl_doc = parser.feed(open('data/text-linux2.hocr',
                                   'r', encoding='utf-8').read())
        print(model.dumps(htl_doc))

    def test_parsing4(self):
        parser = HOCRParser(True)
        htl_doc = parser.feed(open('data/text-linux2.hocr',
                                   'r', encoding='utf-8').read())
        print(model.dump(htl_doc, open("text-linux2.htl", "w+b")))

if __name__ == '__main__':
    unittest.main()
