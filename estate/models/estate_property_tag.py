from odoo import fields,models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag Test"

    name = fields.Char(required=True)
    color = fields.Integer()
    _order = "name "
    _sql_constraints = [
        ('check_name', 'UNIQUE(name )',
         'The TAG NAME must be unique.')
    ]