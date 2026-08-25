# data-converter

Python library that loads JSON, JSON5, XML, YAML, or TOML into a
dictionary, then writes any of those formats.

Install the **`lupaxa-data-converter`** package and import the
`lupaxa.data_converter` namespace:

```bash
pip install lupaxa-data-converter
```

```python
from lupaxa.data_converter import DataConverter

payload = {"name": "Lupaxa", "formats": ["json", "json5", "xml", "yaml", "toml"]}
converter = DataConverter(payload, data_type="dict")
print(converter.to_json())
print(converter.to_toml())
```

`data-converter` is a library only. There is no console script and no
`python -m` entry point.

## What you get

- Load any supported format into a standard Python dictionary
- Dump that dictionary to JSON, JSON5, XML, YAML, or TOML
- No pairwise converters — two passes through the dict hub
- Python 3.10+, with `PyYAML`, `defusedxml`, `json5`, and `tomli-w`

## Next steps

- [Getting started](getting-started.md) — install and first conversions
- [Usage](usage.md) — load types and conversion methods
- [Reference](reference.md) — public API
- [Examples](examples.md) — copy-paste recipes
