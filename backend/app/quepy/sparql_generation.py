# -*- coding: utf-8 -*-

"""
Sparql generation code.
"""

from backend.app.quepy import settings
from backend.app.quepy.dsl import IsRelatedTo
from backend.app.quepy.expression import isnode
from backend.app.quepy.encodingpolicy import assert_valid_encoding

_indent = u"  "


def escape(string):
    string = str(string)
    string = string.replace("\n", "")
    string = string.replace("\r", "")
    string = string.replace("\t", "")
    string = string.replace("\x0b", "")
    if not string or any([x for x in string if 0 < ord(x) < 31]) or \
            string.startswith(":") or string.endswith(":"):
        message = "Unable to generate sparql: invalid nodes or relation"
        raise ValueError(message)
    return string


def adapt(x):
    if isnode(x):
        x = u"?x{}".format(x)
        return x
    if isinstance(x, str):
        assert_valid_encoding(x)
        if x.startswith(u"\"") or ":" in x:
            return x
        return u'"{}"'.format(x)
    return str(x)


def expression_to_sparql(e, full=False):
    template = u"SELECT DISTINCT {select} WHERE {{\n" +\
               u"{expression}\n" +\
               u"}}\n"
    head = adapt(e.get_head())
    print("head")
    print(head)
    if full:
        select = u"*"
    else:
        select = head
    y = 0
    xs = []
    for node in e.iter_nodes():
        print("node",node)
        for relation, dest in e.iter_edges(node):
            print("relation", relation)
            print("dest", dest)
            if relation is IsRelatedTo:
                relation = u"?y{}".format(y)
                y += 1
            print(relation)
            xs.append(triple(adapt(node), relation, adapt(dest),
                      indentation=1))

    sparql = template.format(preamble=settings.SPARQL_PREAMBLE2,
                             select=select,
                             expression=u"\n".join(xs))
    return select, sparql


def triple(a, p, b, indentation=0):
    a = escape(a)
    b = escape(b)
    p = escape(p)
    s = _indent * indentation + u"{0} {1} {2}."
    return s.format(a, p, b)
