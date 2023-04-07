# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from linchemin.__about__ import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LinChemIn'
copyright = '2022 Syngenta Group Co. Ltd.'
author = 'Marco Stenta, Marta Pasquini'
show_authors = True

# Autopopulate version
release = __version__
# The major version (X.Y version).
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
modindex_common_prefix = ["linchemin."]

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.viewcode']

templates_path = ['templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bizstyle'
html_static_path = ['static']
html_logo = "static/linchemin_logo.png"


html_sidebars = {
        '**': [
                 'localtoc.html',
                 'relations.html',
                 'searchbox.html',
                 'authors.html',
            ]
        }
