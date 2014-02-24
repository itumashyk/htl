""" Parser of hOCR files
https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview
"""

__all__ = ['HOCRParser']

from html.parser import HTMLParser
from .model import *


class HOCRParser (HTMLParser):

    _PAGE_CLASSES = ('ocr_page')
    _AREA_CLASSES = ('ocr_linear', 'ocr_carea')
    _PAR_CLASSES = ('ocr_title', 'ocr_author', 'ocr_abstract', 'ocr_display',
        'ocr_blockquote', 'ocr_par', 'ocr_caption', 'ocrx_block')
    _LINE_CLASSES = ('ocr_line', 'ocrx_line')
    _WORD_CLASSES = ('ocrx_word')
    _STACK_IGNORED_TAGS = ('meta', 'img', 'br')

    def __init__(self, verbose=False):
        super().__init__()
        self._tags_stack = []
        self._pages = []
        self._verbose = verbose

    def _log(self, *objects):
        if self._verbose:
            print(*objects)

    def _parse_start_of_class(self, tag, hocr_class):
        if hocr_class in self._PAGE_CLASSES:
            page = HTLPage([])
            page.tag = tag
            self._pages.append(page)
            self._tags_stack.append(page)

        elif hocr_class in self._AREA_CLASSES:
            area = HTLArea([])
            area.tag = tag
            self._tags_stack.append(area)

        elif hocr_class in self._PAR_CLASSES:
            par = HTLPar([])
            par.tag = tag
            self._tags_stack.append(par)

        elif hocr_class in self._LINE_CLASSES:
            line = HTLLine([], '')
            line.tag = tag
            self._tags_stack.append(line)
        elif hocr_class in self._WORD_CLASSES:
            word = HTLWord([], '')
            word.tag = tag
            self._tags_stack.append(word)
        else:
            self._log('hOCR class ignored:', hocr_class)
            self._tags_stack.append(HTLStub(tag))

    def _handle_special_start_tag(self, tag, attrs):
        if tag in self._STACK_IGNORED_TAGS:
            return True

    def handle_starttag(self, tag, attrs):

        attrs_dict = dict(attrs)
        hocr_class = attrs_dict.get('class')

        if hocr_class:
            self._parse_start_of_class(tag, hocr_class)
            return

        if not self._handle_special_start_tag(tag, attrs):
            self._tags_stack.append(HTLStub(tag))

    def handle_endtag(self, tag):
        if tag in self._STACK_IGNORED_TAGS:
            return

        htl_element = self._tags_stack.pop()
        if htl_element.tag != tag:
            print('Tags mismatch in HOCRParser. Expected:<', htl_element.tag,
                  '> but found:<', tag, '>. At line', self.lineno)


    def handle_data(self, data):
        pass