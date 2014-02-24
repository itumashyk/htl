""" Represents document model in htl.
"""

import json
from json import JSONEncoder

__all__ = ['HTLDoc', 'HTLPage', 'HTLArea', 'HTLPar', 'HTLLine', 'HTLWord',
           'HTLStub', 'dump', 'dumps']


class HTLDoc(object):
    def __init__(self, doc_name, pages, lang=None, dc_data=None):
        self._doc_name = doc_name
        self._lang = lang
        self._pages = pages
        self._dc_data = dc_data

    def __repr__(self):
        return '<HTL doc with doc_name: {0}, pages_count: {1}>'.\
            format(self.doc_name,  len(self.pages))


    @property
    def doc_name(self):
        return self._doc_name

    @property
    def lang(self):
        return self._lang

    @property
    def pages(self):
        return self._pages

    @property
    def dc_data(self):
        """ Dublin Core data for document.
        Returns dict.
        """
        return self._dc_data


class HTLBase(object):
    def __init__(self):
        self._type = None
        self._box = None
        self._content_text = None
        self._tag = None
        self._children = []

    def __repr__(self):
        return '<HTL {0} with box: {1}, content_text: "{2}", tag: {3}>'.\
            format(self.type,  self.box, self.content_text, self.tag)

    @property
    def type(self):
        return self._type

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

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag


class HTLPage(HTLBase):
    def __init__(self, box, content_text=None):
        super().__init__()
        self._type = 'page'
        self._box = box
        self._content_text = content_text


class HTLArea(HTLBase):
    def __init__(self, box, content_text=None):
        super().__init__()
        self._type = 'area'
        self._box = box
        self._content_text = content_text


class HTLPar(HTLBase):
    def __init__(self, box, content_text=None):
        super().__init__()
        self._type = 'par'
        self._box = box
        self._content_text = content_text


class HTLLine(HTLBase):
    def __init__(self, box, content_text, char_info=None):
        super().__init__()
        self._type = 'line'
        self._box = box
        self._content_text = content_text
        self._char_info = char_info

    @property
    def char_info(self):
        return self._char_info


class HTLWord(HTLBase):
    def __init__(self, box, content_text, char_info=None):
        super().__init__()
        self._type = 'line'
        self._box = box
        self._content_text = content_text
        self._char_info = char_info

    @property
    def char_info(self):
        return self._char_info

class HTLStub(HTLBase):
    def __init__(self, tag):
        super().__init__()
        self._type = 'stub'
        self._tag = tag

class HTLEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, HTLDoc):
            result = {'doc_name': o.doc_name}

            if o.lang:
                result['lang'] = o.lang

            if o.dc_data:
                result['dc_data'] = o.dc_data

            result['pages'] = o.pages
            return result

        if isinstance(o, HTLBase):
            result = {'type': o.type}

            result['box'] = o.box

            if o.content_text:
                result['content_text'] = o.content_text

            if hasattr(o, 'char_info'):
                result['char_info'] = o.char_info

            if o.children:
                result['children'] = o.children

            return result

        return super().default(o)


def dumps(htl_obj, compact=False):
    if not compact:
        return json.dumps(htl_obj, cls=HTLEncoder, indent=2, ensure_ascii=False)
    return json.dumps(htl_obj, cls=HTLEncoder, separators=(',', ':'), ensure_ascii=False)


def dump(htl_obj, fp, compact=False):
    if not compact:
        return json.dump(htl_obj, fp, cls=HTLEncoder, indent=2, ensure_ascii=False)
    return json.dump(htl_obj, fp, cls=HTLEncoder, separators=(',', ':'), ensure_ascii=False)