# -*- coding: utf-8 -*-
# from odoo import http


# class GestionReservasCine(http.Controller):
#     @http.route('/gestion_reservas_cine/gestion_reservas_cine', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_reservas_cine/gestion_reservas_cine/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_reservas_cine.listing', {
#             'root': '/gestion_reservas_cine/gestion_reservas_cine',
#             'objects': http.request.env['gestion_reservas_cine.gestion_reservas_cine'].search([]),
#         })

#     @http.route('/gestion_reservas_cine/gestion_reservas_cine/objects/<model("gestion_reservas_cine.gestion_reservas_cine"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_reservas_cine.object', {
#             'object': obj
#         })

