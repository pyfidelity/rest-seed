from colander import MappingSchema, SchemaNode, Mapping
from colander import String, Integer
from colander import Invalid, null, deferred, required


class PossiblyEmptyString(String):
    """ colander's `String` type deserializes any "false" values to `null`,
        which makes it impossible to distinguish between a request that
        contains an empty title (in which case the validator should fire)
        and one that doesn't contain the field at all (in which case
        validation should be skipped) """

    def deserialize(self, node, cstruct):
        if not cstruct:
            return cstruct
        return super(PossiblyEmptyString, self).deserialize(node, cstruct)


def required_validator(node, value):
    if not value:
        raise Invalid(node, 'Required')


@deferred
def title_missing(node, kw):
    if kw['request'].method == 'POST':
        return required
    else:
        return null


class NonableMapping(Mapping):

    def serialize(self, node, appstruct):
        if appstruct is null or appstruct is None:
            return None
        else:
            return super(NonableMapping, self).serialize(node, appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is null or cstruct is None:
            return null
        else:
            return super(NonableMapping, self).deserialize(node, cstruct)


class FileSchema(MappingSchema):
    schema_type = NonableMapping
    id = SchemaNode(Integer(), missing=None)
    data = SchemaNode(String(), missing=None)
    filename = SchemaNode(String(), missing=None)
    mimetype = SchemaNode(String(), missing=None)


def MissingOrRequiredNode():
    return SchemaNode(PossiblyEmptyString(), missing=title_missing,
        validator=required_validator)


class ContentSchema(MappingSchema):
    id = SchemaNode(Integer(), missing=None)
    title = MissingOrRequiredNode()
    description = SchemaNode(String(), missing=null)
