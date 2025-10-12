from os import path

import importlib_resources as resources
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file

from .. import static as static_module


def add_js(app: Sphinx):

    print(resources.files(static_module).joinpath("viewer-static.min.js"))

    abs_js_path = resources.files(static_module).joinpath("viewer-static.min.js")

    app.add_js_file(path.basename(abs_js_path), loading_method="defer")


def build_finished(app: Sphinx, _exception):

    copy_asset_file(
        str(resources.files(static_module).joinpath("viewer-static.min.js")),
        path.join(app.builder.outdir, '_static'),
        app.builder)


def init_numfig_format(app, config):

    numfig_format = {"scheme": "Схема %s"}

    numfig_format.update(config.numfig_format)
    config.numfig_format = numfig_format


def setup_svgio(app: Sphinx):

    app.add_config_value("drawio_js_offline_path", "", "html")
    app.connect("config-inited", init_numfig_format)
    app.connect("builder-inited", add_js)
    app.connect('build-finished', build_finished)

    from .directive import setup_directive
    from .node import setup_node
    setup_directive(app)
    setup_node(app)
