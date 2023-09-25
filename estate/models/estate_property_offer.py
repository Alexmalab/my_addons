from odoo import api ,fields,models
from datetime import timedelta
from odoo.exceptions import UserError
class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Type Offer Test"

    price = fields.Float()
    status = fields.Selection( [('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner' ,required=True)
    property_id = fields.Many2one('estate.property' ,required=True)

    # 第8章最后小节
    
    property_type_id = fields.Many2one(
        string='property_type_id',
        comodel_name='estate.property.type',
        related='property_id.property_type_id',
        store =True
    )
    
    #

    _order = "price desc"
    validity = fields.Integer(
        string='Validity',
        default=7
    )
    
    date_deadline = fields.Date(
        string='Date Deadline',
        
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
         )
        
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0.0 )',
         'The offer price must be strictly postive.')
    ]
    
    @api.depends('validity','create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                
                date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                date_deadline = fields.Date.today() + timedelta(days=record.validity)
            
        record.date_deadline = date_deadline
        
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                diff = record.date_deadline - record.create_date.date()
                record.validity = diff.days
            else:
                record.validity = 7
        
        
        
    def action_refuse(self):
        self.status = 'refused'
        return True
    def action_accept(self):
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        return True
    
    #13章 防止创建低于最低报价的off
    @api.model
    def create(self, vals):
        if 'price' in vals and 'property_id' in vals:
            existing_offers = self.env['estate.property.offer'].search([('property_id', '=', vals['property_id'])])
            for offer in existing_offers:
                if vals['price'] < offer.price:
                    raise UserError("无法创建金额低于现有报价的报价。")
        # vals['status'] = 'accepted'
        property = self.env['estate.property'].browse(vals['property_id'])
        property.state = 'offer_received'
        return super(PropertyOffer, self).create(vals)