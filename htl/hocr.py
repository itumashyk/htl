""" Parser of hOCR files
https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview
"""

__all__ = ['HOCRParser']

from html.parser import HTMLParser
from .model import *
import re


class HOCRParser (HTMLParser):

    _PAGE_CLASSES = ('ocr_page')
    _AREA_CLASSES = ('ocr_linear', 'ocr_carea')
    _PAR_CLASSES = ('ocr_title', 'ocr_author', 'ocr_abstract', 'ocr_display',
        'ocr_blockquote', 'ocr_par', 'ocr_caption', 'ocrx_block')
    _LINE_CLASSES = ('ocr_line', 'ocrx_line')
    _WORD_CLASSES = ('ocrx_word')
    _INFO_CLASSES = ('ocr_cinfo', 'ocrx_cinfo')

    _STACK_IGNORED_TAGS = ('meta', 'img', 'br')

    _BBOX_RE = re.compile(r'\bbbox\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
    _X_BBOXES_RE = re.compile(r'\bx_bboxes\s+(.+)\s+')
    _IMAGE_NAME_RE = re.compile(r'\bimage\s+"?([^"]+)"?')

    def __init__(self, verbose=False):
        super().__init__()
        self._tags_stack = []
        self._pages = []
        self._verbose = verbose
        self._name_of_first_page = None

    def _log(self, *objects):
        if self._verbose:
            print(*objects)

    def _parse_start_of_class(self, tag, hocr_class, attrs):
        bbox = self._get_bbox(attrs)
        info = self._get_info(attrs)

        if hocr_class in self._PAGE_CLASSES:
            page = HTLPage(bbox)
            page.tag = tag
            self._pages.append(page)
            self._tags_stack.append(page)
            image_title = self._get_image_name(attrs)
            if not self._name_of_first_page:
                self._name_of_first_page = image_title

        elif hocr_class in self._AREA_CLASSES:
            area = HTLArea(bbox)
            area.tag = tag
            self._find_first_non_stub().add_child(area)
            self._tags_stack.append(area)

        elif hocr_class in self._PAR_CLASSES:
            par = HTLPar(bbox)
            par.tag = tag
            self._find_first_non_stub().add_child(par)
            self._tags_stack.append(par)

        elif hocr_class in self._LINE_CLASSES:
            line = HTLLine(bbox, '')
            line.tag = tag
            line.char_info = info
            self._find_first_non_stub().add_child(line)
            self._tags_stack.append(line)

        elif hocr_class in self._WORD_CLASSES:
            word = HTLWord(bbox, '')
            word.tag = tag
            word.char_info = info
            self._find_first_non_stub().add_child(word)
            self._tags_stack.append(word)

        elif hocr_class in self._INFO_CLASSES:
            self._find_first_non_stub().char_info = info
            self._tags_stack.append(HTLStub(tag))

        else:
            self._log('hOCR class ignored:', hocr_class)
            self._tags_stack.append(HTLStub(tag))

    def _handle_special_start_tag(self, tag, attrs):
        if tag in self._STACK_IGNORED_TAGS:
            return True

    def _find_first_non_stub(self):
        for element in reversed(self._tags_stack):
            if not isinstance(element, HTLStub):
                return element

        return None

    def _get_bbox(self, attrs):
        data_str = attrs.get('title')
        if data_str:
            match = self._BBOX_RE.search(data_str)
            if match:
                return [int(x) for x in match.groups()]

        return []

    def _get_image_name(self, attrs):
        data_str = attrs.get('title')
        if data_str:
            match = self._IMAGE_NAME_RE.search(data_str)
            if match:
                return match.groups()[0]
        return None

    def _get_info(self, attrs):
        data_str = attrs.get('title')
        if data_str:
            match = self._X_BBOXES_RE.search(data_str)
            if match:
                array_str = match.groups()[0]
                return [int(x.strip()) for x in array_str.split(' ')]

        return None

    def handle_starttag(self, tag, attrs):

        attrs_dict = dict(attrs)
        hocr_class = attrs_dict.get('class')

        if hocr_class:
            self._parse_start_of_class(tag, hocr_class, attrs_dict)
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
        if data.strip() == '':
            return

        first_non_stub = self._find_first_non_stub()
        if first_non_stub:
            self._find_first_non_stub().append_text(data)
        else:
            self._log('Ignored text:', repr(data))

    def feed(self, data, doc_name=None):
        super().feed(data)

        if len(self._tags_stack) != 0:
            self._log('Unclosed tag found')

        if not doc_name:
            doc_name = self._name_of_first_page

        return HTLDoc(doc_name, self._pages)