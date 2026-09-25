<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Developers Toolbox" />
  </a>
</p>

<h1 align="center">Data Converter</h1>

Python library that loads JSON, JSON5, XML, YAML, or TOML into a
dictionary, then writes any of those formats.

## Install

```bash
pip install lupaxa-data-converter
```

Requires Python 3.10+.

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

This is a library only. There is no console script and no
`python -m` entry point.

## Documentation

Site pages live in `mkdocs/` and publish to
<https://data-converter.thelupaxaproject.org/>.

```bash
make init
make python-install-dev
make mkdocs-serve
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
