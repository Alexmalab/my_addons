from odoo import fields,models

class EstateAction(models.Model):
    _name = 'estate.action'

    name = fields.Char()

