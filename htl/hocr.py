""" Parser of hOCR files
https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview
"""

__all__ = ['HOCRParser']

from html.parser import HTMLParser

class HOCRParser (HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, "|", attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", repr(data))