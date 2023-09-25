from odoo import models
class EstateProperty(models.Model):
    _inherit = 'estate.property'
    
    def action_sold(self):
        # super().action_sold()
        res = super().action_sold()
        print('test invoice')
        # 添加发票创建逻辑
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,  # Replace with the actual customer ID.
            'move_type': 'out_invoice',  # Replace with the appropriate move type.
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.name,
                    'quantity': 1,  # You can adjust the quantity as needed.
                    'price_unit': self.selling_price * 0.06,  # 6% of the selling price.
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,  # You can adjust the quantity as needed.
                    'price_unit': 100.00,
                }),
            ],
        })
        return res