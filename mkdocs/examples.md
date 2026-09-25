# Examples

## Dictionary to Every Text Format

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

## JSON String to XML and YAML

```python
converter = DataConverter('{"id": 1, "ok": true}', data_type="json")
print(converter.to_xml())
print(converter.to_yaml())
```

## JSON5 to TOML Via the Dict Hub

```python
converter = DataConverter("{ id: 1, ok: true, }", data_type="json5")
print(converter.to_toml())
```

## YAML String to a Dictionary

```python
data = DataConverter.yaml_to_dict("name: Lupaxa\nactive: true\n")
print(data["name"])
```

## XML String to JSON

```python
print(DataConverter.xml_to_json("<root><id>1</id></root>"))
# {"id": "1"}
```

## Dictionary to XML With a Custom Root

```python
print(DataConverter.dict_to_xml({"id": 1}, root_tag="item"))
```
