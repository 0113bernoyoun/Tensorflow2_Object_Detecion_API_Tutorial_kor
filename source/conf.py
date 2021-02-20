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
import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'Tensorflow2 Object Detection API Guide'
copyright = '2021, BernoYoun'
author = 'BernoYoun'

# The full version, including alpha/beta/rc tags
release = '0.0'
version = ''

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    "sphinx_rtd_theme",
    'sphinx.ext.autodoc',
    'sphinx.ext.imgmath',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

source_suffix = ['.rst', '.md']
master_doc = 'index'
language = None
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'Sphinx-Tutorialdoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'Sphinx-Tutorial.tex', 'Sphinx-Tutorial Documentation',
     'Sooftware', 'manual'),
]
man_pages = [
    (master_doc, 'sphinx-tutorial', 'Sphinx-Tutorial Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'Sphinx-Tutorial', 'Sphinx-Tutorial Documentation',
     author, 'Sphinx-Tutorial', 'One line description of project.',
     'Miscellaneous'),
]
epub_title = project
epub_exclude_files = ['search.html']
intersphinx_mapping = {'https://docs.python.org/': None}
todo_include_todos = True