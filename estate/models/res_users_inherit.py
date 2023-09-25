from odoo import fields,models

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        string='salesman_id',
        comodel_name='estate.property',
        inverse_name='salesman_id',
        domain=[('state', 'in', ['new', 'offer_received'])]
    )
    