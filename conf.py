# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'Big Anchoring Machine Learning Module'
copyright = '2024, ICA'
author = 'ICA'
release = 'alpha_01'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'pt'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Opcional: Se desejar, você pode remover o título do projeto da barra de navegação:
# html_theme_options = {
#     "logo_only": True,
#     "display_version": False,
# }

# -- Options for LaTeX output ------------------------------------------------
latex_engine = 'pdflatex'  # Define o engine LaTeX, pdflatex é o mais comum.

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'''
    \usepackage{babel}  % Para suporte ao idioma, como português.
    \usepackage{amsmath, amssymb, amsfonts}  % Pacotes matemáticos adicionais.
    \usepackage{graphicx}  % Para inserir gráficos e imagens.
    \usepackage{enumitem}  % Para listas personalizadas.
    \setcounter{tocdepth}{2}  % Define a profundidade do sumário.
    ''',

    # Figure alignment
    'figure_align': 'H',  # Controla o alinhamento das figuras.

    # Nome personalizado da versão na documentação
    'releasename': 'Versão',
}

# Nome do documento principal gerado no LaTeX, geralmente igual ao nome do projeto.
latex_documents = [
    ('index', 'BigAnchoringMachineLearningModule.tex',
     'Big Anchoring Machine Learning Module Documentation',
     'ICA', 'manual'),
]
