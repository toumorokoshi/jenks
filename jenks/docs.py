import os

readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')

with open(readme_path, 'r') as fh:
    README_CONTENT = fh.read()

DOCS = """
{readme}

Usage
=====

{usage}
""".strip()
