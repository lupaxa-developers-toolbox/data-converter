# Getting started

## Requirements

- Python 3.10 or newer
- `PyYAML`, `defusedxml`, `json5`, and `tomli-w` (installed with the package)
- `tomli` on Python 3.10 (3.11+ uses stdlib `tomllib`)

## Install

```bash
python3 -m pip install lupaxa-data-converter
```

Then import the namespace:

```python
from lupaxa.data_converter import DataConverter
```

The PyPI name is `lupaxa-data-converter`. The import path is
`lupaxa.data_converter`. `lupaxa` is a namespace package — there is no
`lupaxa/__init__.py`.

This is a library only. There is no console script and no
`python -m lupaxa.data_converter` entry point.

### From source (development)

Editable install with dev extras (includes the MkDocs pins):

```bash
make init
make python-install-dev
```

Site Markdown lives in `mkdocs/` (not GitHub’s special `docs/` directory).
After makefile-skills are installed:

```bash
make mkdocs-serve
```

## First conversion

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

Load a document string by passing `data_type` as `json`, `json5`, `xml`,
`yaml`, or `toml`. The value is always stored as a dictionary, then any
`to_*` method can write it out.

## Makefile helpers

```bash
make init                 # clone makefile-skills into .makefiles/
make python-install-dev   # editable install with [dev]
make python-check         # lint + type + test (via makefile-skills)
make mkdocs-serve         # local docs site
```
