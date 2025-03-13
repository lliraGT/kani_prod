# models/stock_move.py
from odoo import models, fields, api # type: ignore

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    # Keep the field but make it a computed field that returns 0
    # This avoids validation while keeping the field for view compatibility
    x_studio_actual_weight = fields.Float(
        string='Peso Real',
        compute='_compute_dummy_weight',
        store=False,
        help='Campo mantenido por compatibilidad'
    )
    
    def _compute_dummy_weight(self):
        for move in self:
            move.x_studio_actual_weight = 0.0