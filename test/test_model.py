import unittest
from unittest import TestCase
from htl.model import HTLDoc
from htl.model import HTLPage
from htl.model import HTLLine
from htl import model


class ModelTestCase(TestCase):
    @unittest.skip
    def test_simple(self):
        line = HTLLine([1, 2, 3, 4], "text", [1, 2, 3, 4, 5])
        page = HTLPage([1, 1, 1, 1])
        page.add_child(line)
        doc = HTLDoc('test.png', [page], 'EN')
        print(str(doc))
        print(model.dumps(doc, False))

if __name__ == '__main__':
    unittest.main()