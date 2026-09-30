<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Developers Toolbox" />
  </a>
</p>

<h1 align="center">Data Converter</h1>

Python library that loads JSON, JSON5, XML, YAML, or TOML into a
dictionary, then writes any of those formats. Conversion is two-pass
through that dict hub — there are no pairwise converters.

The PyPI name is `lupaxa-data-converter`. The import path is
`lupaxa.data_converter`. `lupaxa` is a namespace package.

## Install

```bash
pip install lupaxa-data-converter
```

Requires Python 3.10+. The package pulls in `PyYAML`, `defusedxml`,
`json5`, and `tomli-w`. Python 3.10 also needs `tomli`; 3.11+ uses
stdlib `tomllib`.

This is a library only. There is no console script and no
`python -m` entry point.

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

`DataConverter` accepts a dictionary or a document string. Set
`data_type` to match the input (case-insensitive). The value is always
stored as a mapping on `converter.data`, then any `to_*` method can
write it out. Identity conversions are supported.

| `data_type` | Input                          |
| ----------- | ------------------------------ |
| `dict`      | A Python dictionary            |
| `json`      | A JSON object string (default) |
| `json5`     | A JSON5 object string          |
| `xml`       | An XML document string         |
| `yaml`      | A YAML mapping string          |
| `toml`      | A TOML table string            |

```python
from_dict = DataConverter({"id": 1}, data_type="dict")
from_json = DataConverter('{"id": 1}', data_type="json")
from_json5 = DataConverter("{ id: 1, }", data_type="json5")
from_xml = DataConverter("<root><id>1</id></root>", data_type="xml")
from_yaml = DataConverter("id: 1\n", data_type="yaml")
from_toml = DataConverter("id = 1\n", data_type="toml")
```

JSON, JSON5, YAML, and TOML documents must be mappings. Arrays and
scalars raise `DataConverterError`.

`to_xml()` wraps the mapping in `root_tag` (the XML source root, or
`root` for other sources). Pass `root_tag` to override it.

```python
converter.to_xml(root_tag="item")
```

### XML

Child elements with the same tag become a list. Attributes are stored
as `@name` keys and written back as attributes. A list value is
emitted as repeated elements with that key. The original root stays
on `converter.root_tag`.

```python
converter = DataConverter('<person id="7"><name>Ann</name></person>', data_type="xml")
converter.data
# {"@id": "7", "name": "Ann"}
converter.to_xml()
# <person id="7">...</person>
```

### Errors

Parse failures, type mismatches, unsupported `data_type` values, and
invalid XML names raise `DataConverterError`. Underlying parser errors
are attached as `__cause__`.

```python
from lupaxa.data_converter import DataConverter, DataConverterError

try:
    DataConverter("{not-json", data_type="json")
except DataConverterError as exc:
    print(exc)
```

### Helpers

These class methods convert without constructing an instance first.
`dict_to_xml` and `json_to_xml` wrap the mapping in `root_tag`
(default `root`). `xml_to_json` returns the element payload, not a
`{root: ...}` wrapper.

```python
from lupaxa.data_converter import DataConverter

DataConverter.dict_to_xml({"id": 1}, root_tag="root")
DataConverter.json_to_xml({"id": 1}, root_tag="root")
DataConverter.xml_to_json("<root><id>1</id></root>")
DataConverter.yaml_to_dict("id: 1\n")
DataConverter.toml_to_dict("id = 1\n")
DataConverter.json5_to_dict("{ id: 1, }")
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
