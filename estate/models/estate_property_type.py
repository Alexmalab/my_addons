from odoo import api, fields,models

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property  Type test '
    _order = "name "
    name = fields.Char('Property Type',required = True )
    sequence = fields.Integer('Sequence')
    description = fields.Char('Property Type test')
    property_ids = fields.One2many(
        string='property',
        comodel_name='estate.property',
        inverse_name='property_type_id',
    )
    #xin
    
    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
    )
    
    offer_count = fields.Integer(
        string='offer_count',
        compute='_compute_offer_count' )
        
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        
    def action_open_offers_method(self):
        return self.env.ref('estate.action_open_offers').read()[0]    
        
    
    #
    _sql_constraints = [
        ('check_name', 'UNIQUE(name )',
         'The offer TYPE NAME must be unique.')
    ]
    

    
    
    