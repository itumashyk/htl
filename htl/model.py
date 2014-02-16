""" Represents document model in htl.
"""

__all__ = ['HTLDoc', 'HTLPage', 'HTLArea', 'HTLPar', 'HTLLine', 'HTLWord']

class HTLDoc(object):
    def __init__(self, doc_name, lang, pages):
        self._doc_name = doc_name
        self._lang = lang
        self._pages = pages

class HTLBase(object):
    def __init__(self):
        self._name = None
        self._box = None
        self._content_text = None
        self._children = []

    @property
    def name(self):
        return self._name

    @property
    def box(self):
        return self._box

    @property
    def content_text(self):
        return self._content_text

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

class HTLPage(HTLBase):
    def __init__(self, box, content_text=None):
        super().__init__()
        self._name = 'page'
        self._box = box
        self._content_text = content_text

class HTLArea(HTLBase):
    def __init__(self, box, content_text=None):
        super().__init__()
        self._name = 'area'
        self._box = box
        self._content_text = content_text

class HTLPar(HTLBase):
    def __init__(self, box, content_text=None):
        super().__init__()
        self._name = 'par'
        self._box = box
        self._content_text = content_text

class HTLLine(HTLBase):
    def __init__(self, box, content_text, char_info=None):
        super().__init__()
        self._name = 'line'
        self._box = box
        self._content_text = content_text
        self._char_info = char_info

    @property
    def char_info(self):
        return self._char_info

class HTLWord(HTLBase):
    def __init__(self, box, content_text, char_info=None):
        super().__init__()
        self._name = 'line'
        self._box = box
        self._content_text = content_text
        self._char_info = char_info

    @property
    def char_info(self):
        return self._char_info