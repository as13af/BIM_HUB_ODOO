# -*- coding: utf-8 -*-
# from odoo import http


# class BimProject(http.Controller):
#     @http.route('/bim_project/bim_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bim_project/bim_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bim_project.listing', {
#             'root': '/bim_project/bim_project',
#             'objects': http.request.env['bim_project.bim_project'].search([]),
#         })

#     @http.route('/bim_project/bim_project/objects/<model("bim_project.bim_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bim_project.object', {
#             'object': obj
#         })
