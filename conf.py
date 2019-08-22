# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Project information -----------------------------------------------------
project = 'Kamuee Project'
copyright = '2019, NTT Communications'
author = 'Hiroki Shirokura'
version = '0.0.0'
release = '0.0.0'

# -- General configuration ---------------------------------------------------
title = 'Kamuee User\'s guide'
extensions = [ 'sphinx.ext.todo' ]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'ja'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = None

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'KamueeProjectdoc'

# -- Options for LaTeX output ------------------------------------------------
latex_elements = { 'extraclassoptions': 'openany' }
latex_documents = [
    (master_doc, 'users_guide.tex', title,
     'Hiroki Shirokura', 'manual'),
]
latex_docclas = {'manual': 'jsbook'}


# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, 'kamueeproject', 'Kamuee Project Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'KamueeProject', title,
     author, 'KamueeProject', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_exclude_files = ['search.html']
