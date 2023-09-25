from odoo import api,fields,models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property test '
    _order = 'id desc'

    name = fields.Char('Property Name',required = True )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Availability date',default = fields.Date.today(),copy = False)
    expected_price = fields.Float(required = True)
    selling_price =fields.Float(readonly = True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer(compute='_compute_garden_area' ,readonly=False)
    state = fields.Selection(
        string='Status',
        selection=[ ('new','New'), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'),('sold','Sold'),  ('canceled','Canceled')],
        help=" State of the property",
        default = 'new',
        copy = False,
        required=True
    )
    garden_orientation = fields.Selection(
        compute='_compute_garden_orientation',
        readonly=False, 
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation of the property"
    )

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0.0 )',
         'The expected price must be strictly postive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0.0 )',
         'The selling price must be postive.')
    ]


    property_type_id = fields.Many2one('estate.property.type',string="Property Type")
    buyer_id = fields.Many2one('res.partner',string = 'Buyer',copy=False,readonly=True)
    salesman_id = fields.Many2one('res.users',string = 'Salesman',default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag',string="Property Tags")
    offer_ids =  fields.One2many('estate.property.offer','property_id',string='Offer')
    total_area = fields.Integer(compute='_compute_total_area',readonly = True)

    best_price = fields.Float(
        compute='_compute_best_price', string='Best Offer',readonly = True,copy=False)
    
    
    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price<record.expected_price*0.9:
                raise ValidationError('the selling price cannot lower than 90 percent of the expected price.')
            
    
    
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            print(prices)
            record.best_price= max(prices) if prices else 0
    
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    
    @api.depends('garden')
    def _compute_garden_area(self):
        for record in self:
            if record.garden == True:
                record.garden_area = 10
            else:
                record.garden_area = 0
                
    
    
    @api.depends('garden')
    def _compute_garden_orientation(self):
        for record in self:
            if record.garden == True:
                record.garden_orientation = 'north'
            else:
                record.garden_orientation = False
    
    
    

    def action_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("已取消房源无法设置为已售")
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state !='sold':
                record.state = 'canceled'
            else:
                raise UserError("已售房源无法取消")
        return True
    
    #13章内容
    def unlink(self):
        for record in self:
            if record.state  not in ['new', 'canceled']:
                raise UserError("无法删除状态不是'New'或'Canceled'的房产。")
        return super(Property, self).unlink() 

    #