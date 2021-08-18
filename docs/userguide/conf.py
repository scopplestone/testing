import sphinx_rtd_theme

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

master_doc = 'index'
project = 'PICLas Testing'
copyright = '2021, Stephen Copplestone'
author = 'University of Stuttgart, Institute for Aerodynamics and Gas Dynamics (IAG), Institute for Space Systems (IRS), boltzplatz - Numerical Plasma Dynamics'
# latex config
latex_documents = [
    (master_doc, 'foo.tex', 'Project',
     author.replace(', ', '\\and ').replace(' and ', '\\and and '),
     'manual'),
]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.autosectionlabel',
        'sphinxcontrib.bibtex',
        'sphinx_rtd_theme',
        'myst_parser'
        ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    # Toc options
    'collapse_navigation': False,
    'navigation_depth': 4,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '../logo.png'

# -- Bibliography ------------------------------------------------------------

bibtex_bibfiles = ['../references.bib']

# -- Section labelling -------------------------------------------------------
# Make sure the target is unique
autosectionlabel_prefix_document = True

# Activate using: {numref}`tab:some-name` -> Table 1
numfig = True