{
    'name': 'Real Estate ni Karl 1',
    'version': '1.0',
    'sequence': 1,
    'category': 'Real Estate',
    'summary': 'Real Estate of Karl',
    'description': "",
    'website': 'https://google.com',
    'depends': [
            'base'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',

        'views/estate_menus.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}