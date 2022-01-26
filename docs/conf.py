# Configuration file for the Sphinx documentation builder.
from __future__ import annotations

import os
import sys

from sphinx_pyproject import SphinxConfig

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root directory to module search paths
sys.path.insert(0, root_dir)

# Loan configurations from pyproject.toml
config = SphinxConfig(os.path.join(root_dir, "pyproject.toml"), globalns=globals())

# Sphinx plugins configurations
autosectionlabel_prefix_document = True
autodoc_member_order = 'bysource'
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
