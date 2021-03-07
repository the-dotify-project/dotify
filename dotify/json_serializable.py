import json

from python_jsonschema_objects import ObjectBuilder


class JsonSerializableMeta(type):
    def __new__(cls, name, bases, attrs):
        if 'schema' in attrs:
            with attrs['schema'].open() as file:
                json_schema = json.load(file)

                builder = ObjectBuilder(json_schema)
                classes = builder.build_classes(
                    strict=True,
                    named_only=True,
                    standardize_names=False
                )

                dto_class = getattr(classes, name)

            attrs['dto_class'] = dto_class

        return super().__new__(cls, name, bases, attrs)


class JsonSerializable(object, metaclass=JsonSerializableMeta):
    def __init__(self, **kwargs):
        dto = self.dto_class(**kwargs)

        self.__dict__.update(
            dto.__dict__['_extended_properties']
        )

        self.__dict__.update(
            dto.__dict__['_properties']
        )
