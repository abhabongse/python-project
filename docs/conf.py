# Configuration file for the Sphinx documentation builder.
from __future__ import annotations

import datetime as dt
import os
import sys

from sphinx_pyproject import SphinxConfig

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root directory to module search paths
sys.path.insert(0, os.path.join(root_dir, "src"))

# Loan configurations from pyproject.toml
name = None  # will be populated by SphinxConfig
author = None  # will be populated by SphinxConfig
version = None  # will be populated by SphinxConfig
config = SphinxConfig(os.path.join(root_dir, "pyproject.toml"), globalns=globals())

# Additional configurations
project = name
project_copyright = f"{dt.date.today().year}, {author} ({version})"
release = version

# Sphinx plugins configurations
autosectionlabel_prefix_document = True
autodoc_member_order = 'bysource'
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
