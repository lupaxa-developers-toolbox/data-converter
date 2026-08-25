# Usage

## Load a value

`DataConverter` accepts a dictionary or a document string. Set `data_type`
to match the input. The name is case-insensitive. Every source is stored
as a Python dictionary, then any `to_*` method can write it out.

| `data_type` | Input                                              |
| ----------- | -------------------------------------------------- |
| `dict`      | A Python dictionary                                |
| `json`      | A JSON object string (default)                     |
| `json5`     | A JSON5 object string                              |
| `xml`       | An XML document string                             |
| `yaml`      | A YAML mapping string                              |
| `toml`      | A TOML table string                                |

```python
from lupaxa.data_converter import DataConverter

from_dict = DataConverter({"id": 1}, data_type="dict")
from_json = DataConverter('{"id": 1}', data_type="json")
from_json5 = DataConverter("{ id: 1, }", data_type="json5")
from_xml = DataConverter("<root><id>1</id></root>", data_type="xml")
from_yaml = DataConverter("id: 1\n", data_type="yaml")
from_toml = DataConverter("id = 1\n", data_type="toml")
```

JSON, JSON5, YAML, and TOML documents must be mappings. Arrays and scalars raise
`DataConverterError`. The loaded mapping is on `converter.data`. XML
keeps the original root on `converter.root_tag`.

## Convert the loaded value

Once constructed, call the matching `to_*` method. Identity conversions
are supported — a JSON source can call `to_json()`, and so on.

```python
converter = DataConverter({"id": 1}, data_type="dict")
converter.to_json()
converter.to_json5()
converter.to_xml()
converter.to_xml(root_tag="item")
converter.to_yaml()
converter.to_toml()
```

Each method returns a string. `to_xml()` wraps the mapping in `root_tag`
(the XML source root, or `root` for other sources). Pass `root_tag` to
override it.

## XML details

Child elements with the same tag become a list. Attributes are stored as
`@name` keys and written back as attributes. A list value is emitted as
repeated elements with that key.

```python
converter = DataConverter('<person id="7"><name>Ann</name></person>', data_type="xml")
converter.data
# {"@id": "7", "name": "Ann"}
converter.to_xml()
# <person id="7">...</person>
```

## Errors

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

## Round-trip helpers

These class methods convert without constructing an instance first:

```python
from lupaxa.data_converter import DataConverter

DataConverter.dict_to_xml({"id": 1}, root_tag="root")
DataConverter.json_to_xml({"id": 1}, root_tag="root")
DataConverter.xml_to_json("<root><id>1</id></root>")
DataConverter.yaml_to_dict("id: 1\n")
DataConverter.toml_to_dict("id = 1\n")
DataConverter.json5_to_dict("{ id: 1, }")
```

`dict_to_xml` and `json_to_xml` wrap the mapping in `root_tag` (default
`root`). `xml_to_json` returns the element payload, not a `{root: ...}`
wrapper.
