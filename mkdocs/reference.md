# Reference

Public names are exported from `lupaxa.data_converter`.

## Package

| Name                 | Description                        |
| -------------------- | ---------------------------------- |
| `__version__`        | Package version string             |
| `get_version()`      | Return `__version__`               |
| `DataConverter`      | Load a value and convert formats   |
| `DataConverterError` | Raised when a conversion fails     |

There is no console script and no `python -m lupaxa.data_converter` entry
point.

`lupaxa` is a namespace package. There is no `lupaxa/__init__.py`.

## DataConverter

| Name                                      | Role                                         |
| ----------------------------------------- | -------------------------------------------- |
| `DataConverter(data, data_type="json")`   | Load a supported document or dictionary      |
| `data`                                    | The loaded mapping                           |
| `data_type`                               | Normalized source type                       |
| `root_tag`                                | XML root used by `to_xml()`                  |
| `to_json()`                               | Return the loaded value as a JSON string     |
| `to_json5()`                              | Return the loaded value as a JSON5 string    |
| `to_xml(root_tag=None)`                   | Return the loaded value as an XML string     |
| `to_yaml()`                               | Return the loaded value as a YAML string     |
| `to_toml()`                               | Return the loaded value as a TOML string     |
| `dict_to_xml(data, root_tag="root")`      | Convert a dictionary to XML                  |
| `json_to_xml(json_data, root_tag="root")` | Convert a JSON object (dict) to XML          |
| `xml_to_json(xml_data)`                   | Convert an XML string to a JSON object       |
| `yaml_to_dict(yaml_data)`                 | Parse a YAML string to a dictionary          |
| `toml_to_dict(toml_data)`                 | Parse a TOML string to a dictionary          |
| `json5_to_dict(json5_data)`               | Parse a JSON5 string to a dictionary         |

`data_type` must be one of `json`, `json5`, `xml`, `yaml`, `toml`, or
`dict` (any case). JSON, JSON5, YAML, and TOML inputs must be mappings.
XML input is parsed with `defusedxml`. TOML is read with `tomllib`
(Python 3.11+) or `tomli` (3.10), and written with `tomli-w`.

## DataConverterError

Subclass of `Exception`. Raised when `data_type` is unsupported, the
value has the wrong Python type, a document cannot be parsed, a document
is not a mapping, or a dictionary key is not a valid XML name.

The default message is `Data conversion error.` Parser exceptions are
available as `__cause__`.
