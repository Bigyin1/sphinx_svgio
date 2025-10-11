import string

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class list_item_node(nodes.General, nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)

        self.page_id = attributes["page_id"]


def visit_list_item(self, node: list_item_node):

    tmpl = string.Template(
        '<div page=$page_id style="order: $page_id">\n'
    )

    mxgraph = tmpl.substitute(page_id=node.page_id)
    self.body.append(mxgraph)


def depart_list_item(self, node):
    self.body.append("</div>\n")


class SvgioListItemDirective(SphinxDirective):

    option_spec = {
        "page": directives.positive_int,
    }

    required_arguments = 0
    has_content = True

    def run(self):

        node = list_item_node(page_id=self.options.get("page")-1)

        self.set_source_info(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class list_node(nodes.General, nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)

        self.diagram_name = attributes["diagram_name"]


def visit_list(self, node: list_node):

    tmpl = string.Template(
        '<div diagram_name=$diagram_name '
        'style="display: flex; '
        'flex-direction: column;">'
    )

    mxgraph = tmpl.substitute(diagram_name=node.diagram_name)
    self.body.append(mxgraph)


def depart_list(self, node):
    self.body.append("</div>\n")


class SvgioListDirective(SphinxDirective):

    option_spec = {
        "name": directives.unchanged_required,
    }

    required_arguments = 0
    has_content = True

    def run(self):

        node = list_node(diagram_name=self.options.get("name"))

        self.set_source_info(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def setup_svgio_list(app: Sphinx):

    app.add_node(
        list_node,
        html=(visit_list, depart_list),
    )
    app.add_node(
        list_item_node,
        html=(visit_list_item, depart_list_item),
    )
    app.add_directive("svgio-list", SvgioListDirective)
    app.add_directive("svgio-item", SvgioListItemDirective)
