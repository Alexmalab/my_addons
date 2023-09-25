{
    'name': 'Real Estate',
    'description': 'Real Estate APP',
    'license':'LGPL-3',
    'author': 'Alex',
    'depends': ['base'],
    'application': True,
    'data':[
        'security/ir.model.access.csv',
        'views/estate_action.xml',          #Odoo对于导入顺序有讲究。
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',     
        'views/estate_property_offer_views.xml',     
        'views/estate_menus.xml', 
        'views/user_form_inherit.xml'
    ],
}