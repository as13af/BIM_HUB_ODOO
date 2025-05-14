from odoo import http
from odoo.http import request

class JwtProtectedController(http.Controller):

    @http.route('/api/my_protected_endpoint', type='json', auth='jwt', methods=['POST'], csrf=False)
    def my_protected_endpoint(self, **kwargs):
        user = request.env.user
        return {
            'message': f'Hello, {user.name}! You have accessed a protected endpoint.',
            'user_id': user.id,
        }
