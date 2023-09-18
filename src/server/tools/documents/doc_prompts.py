from enum import Enum


class Modes:
    SEARCH = 'search'


SEARCH = """
    This tool is useful when you need to search vector embedded documents. 
    The input to this tool is a string for the question to be asked, and will be passed into Doc's `search` function.
    For example, to search for documents with cosine similarity to "hello world", you would pass in the following string: "hello world"
    """
