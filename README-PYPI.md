<!-- markdownlint-disable -->
<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Project Logo" width="256"/><br/>
  </a>
</p>
<h3 align="center">
  The Lupaxa Developers Toolbox<br />
  Part of The Lupaxa Project
</h3>

<br />

# lupaxa-data-converter

Python library that loads JSON, JSON5, XML, YAML, or TOML into a
dictionary, then writes any of those formats.

Built for scripts and tools used by The Lupaxa Project.

The PyPI name is `lupaxa-data-converter`. The import path is
`lupaxa.data_converter`. This is a library only — there is no console
script and no `python -m` entry point.

## Features

- Load JSON, JSON5, XML, YAML, TOML, or a dictionary into one `DataConverter`
- Dump the loaded mapping to any of those formats
- Two passes through a standard dict — no pairwise converters
- Fully typed, linted, formatted, and tested

## Installation

### From PyPI

```bash
pip install lupaxa-data-converter
```

### From source (development mode)

```bash
pip install -e ".[dev]"
```

Requires Python 3.10+. Runtime dependencies: `PyYAML`, `defusedxml`,
`json5`, and `tomli-w` (`tomli` on Python 3.10).
`lupaxa` is a namespace package — there is no `lupaxa/__init__.py`.

## Usage

```python
from lupaxa.data_converter import DataConverter

payload = {"name": "Lupaxa", "formats": ["json", "json5", "xml", "yaml", "toml"]}
converter = DataConverter(payload, data_type="dict")

print(converter.to_json())
print(converter.to_json5())
print(converter.to_xml())
print(converter.to_yaml())
print(converter.to_toml())
```

## Development

Clone the repository and install with Make:

```bash
make init                # first-time makefile-skills checkout
make python-install-dev  # editable install with [dev]
make python-check        # lint, type-check, and test
make mkdocs-serve        # local docs site
```

Documentation: <https://data-converter.thelupaxaproject.org/>.

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
