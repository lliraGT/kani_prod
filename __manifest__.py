# __manifest__.py
{
    'name': 'Kani Manufacturing',
    'version': '17.0.1.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Enhance manufacturing for pet food production',
    'depends': ['mrp', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_views.xml',
        'views/mrp_production_views.xml',
        'views/production_control_wizard_views.xml',
        'views/production_wizard_actions.xml', 
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}