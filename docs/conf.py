"""Sphinx configuration for the cmdcraft documentation."""

project = "cmdcraft"
copyright = "2026, A. M. Weinsen Jr"
author = "A. M. Weinsen Jr"
release = "0.0.8"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": False,
    "show-inheritance": True,
    "inherited-members": True,
}

autodoc_typehints = "description"
napoleon_google_docstring = True
autosummary_generate = True
autosummary_imported_members = False

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = f"{project} {release} documentation"

# Explicit root doc (Sphinx defaults to 'index' but be explicit).
root_doc = "index"
