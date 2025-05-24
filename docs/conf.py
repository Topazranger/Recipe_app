import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Assumes conf.py is in docs/, and code is in root

project = 'Recipe App'
author = 'Your Name'
release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # For Google/NumPy docstrings
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'  # Or try 'sphinx_rtd_theme' if installed
html_static_path = ['_static']