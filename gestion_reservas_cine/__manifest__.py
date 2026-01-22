# -*- coding: utf-8 -*-
{
    'name': "Gestion Reservas Cine",

    'summary': "Módulo para la gestión de reservas en el cine",

    'description': """
Módulo de gestión de reservas para un cine.
Permite gestionar servicios, clientes y reservas,
incluyendo cálculo automático de precios y futura
integración con facturación
    """,

    'author': "Javier, Fran y Andrii",
    'website': "https://github.com/N16K-ed/Modulo_SGEM_EV2",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

