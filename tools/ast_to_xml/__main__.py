import ast
import re
import sys
from xml.dom import minidom

from xml.etree import ElementTree as etree


def prettify(xml_string):
    reparsed = minidom.parseString(xml_string)
    return reparsed.toprettyxml(indent="    ")


"""\
self.parent_element = etree.SubElement(self.parent_element, self.last_name)
self.parent_element.attrib.update({"name": node.__class__.__name__})"""


class ast2xml(ast.NodeVisitor):
    def __init__(self, tree):
        self.root = etree.Element("ast")
        self.last_name = "module"
        self.visit(tree)

    def __str__(self):
        return etree.tostring(self.root)

    def visit(self, node):
        return super().visit(node)


def main(fpath, fout):
    with open(fpath, "r") as f, open(fout, "w") as out_file:
        tree = ast.parse(f.read())
        res = ast2xml(tree)
        out_file.write(prettify(str(res)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
