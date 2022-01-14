from django.db import models


def createsetter(Model:models.Model,data:dict) -> models.Model:
    attribs_modifier = {}
    for attr, val in data.items():
        if hasattr(Model, attr):
            field = Model._meta.get_field(attr)
            if (
                field.one_to_many
                or field.many_to_many
                or field.many_to_one
                or field.one_to_one
            ):
                attribs_modifier[f"{attr}_id"] = val
            else:
                attribs_modifier[attr] = val

    return Model(**attribs_modifier)

def updatesetter(Model:models.Model,data:dict) -> models.Model:
    for attr, val in data.items():
        if hasattr(Model, attr):
            field = Model._meta.get_field(attr)
            if (
                field.one_to_many
                or field.many_to_many
                or field.many_to_one
                or field.one_to_one
            ):
                attr = f"{attr}_id"
            setattr(Model, attr, val)
    return Model