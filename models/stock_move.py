# models/stock_move.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    x_studio_actual_weight = fields.Float(
        string='Peso Real',
        help='Peso real del movimiento de stock'
    )

    @api.constrains('x_studio_actual_weight')
    def _check_actual_weight(self):
        for move in self:
            if move.x_studio_actual_weight < 0:
                raise ValidationError('El peso real no puede ser negativo')