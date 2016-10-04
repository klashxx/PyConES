# -*- coding: utf-8 -*-
#pylint: skip-file


import sys
import os


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('..'))


extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.napoleon',
]


autodoc_default_flags = ["members", "show-inheritance"]
autodoc_member_order = "bysource"
templates_path = ['_templates']

source_suffix = '.rst'

source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'rspace'
copyright = u'GPL'

version = '0.1'
release = '0.1'
language = 'en'

today_fmt = '%d de %B , %Y'

exclude_patterns = ['_build']

show_authors = True

pygments_style = 'sphinx'
html_title = 'rspace Docs'
html_short_title = 'rspace Docs'
html_last_updated_fmt = '%d de %B , %Y'
html_domain_indices = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
htmlhelp_basename = 'rspacedoc'

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'rspace', u'cptab Docs',
   u'Juan Diego Godoy Robles', 'rspace', 'PyConES 2016 - Almería',
   'Miscellaneous'),
]


