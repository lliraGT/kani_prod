# models/mrp_production.py
from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    cooking_temp = fields.Float(string='Temperatura de Cocción (°C)')
    weight_mp = fields.Integer(string='Minutos de pesado de materia prima')  # Keep temporarily
    fridge_lbs = fields.Float(string='Libras entregadas a refrigerado')
    fridge_temp = fields.Float(string='Temperatura de alimento al ingresar a refrigerado (°C)')
    preformado_temp = fields.Float(string='Temperatura de Preformado (°C)')
    formado_type = fields.Selection([
        ('tortas', 'Tortas'),
        ('bites', 'Bites')
    ], string='Tipo de Formado')
    formado_qty = fields.Integer(string='Cantidad de producto')
    weight_verif = fields.Float(string='Verificación de Peso')
    merma_verif = fields.Float(string='Merma por lote', default=0.0)
    freezing_temp = fields.Float(string='Temperatura de congelación (°C)')
    batch_lbs = fields.Float(string='Libras por lote')
    packing_time = fields.Integer(string='Tiempo de empaque')
    batch_bags = fields.Integer(string='Bolsas por lote')
    pt_freeze_temp = fields.Float(string='Temperatura de congelación de producto terminado (°C)')
    batch_observations = fields.Text(string='Observaciones o Variantes del Lote')
    
    # New fields for ingredient weights
    pierna_weight = fields.Float(string='Peso de Pierna y cuadril (lbs)', default=80.0)
    higado_weight = fields.Float(string='Peso de Hígado res (lbs)', default=20.0)
    arroz_weight = fields.Float(string='Peso de Arroz (lbs)', default=14.0)
    avena_weight = fields.Float(string='Peso de Avena (lbs)', default=10.0)
    chia_weight = fields.Float(string='Peso de Chía (lbs)', default=4.0)
    guicoyitos_weight = fields.Float(string='Peso de Guicoyitos (lbs)', default=12.0)
    acelga_weight = fields.Float(string='Peso de Acelga (lbs)', default=13.0)
    brocoli_weight = fields.Float(string='Peso de Brócoli (lbs)', default=13.0)
    apio_weight = fields.Float(string='Peso de Apio (lbs)', default=4.0)
    papas_weight = fields.Float(string='Peso de Papas (lbs)', default=8.0)
    zanahoria_weight = fields.Float(string='Peso de Zanahoria (lbs)', default=10.0)
    camote_weight = fields.Float(string='Peso de Camote (lbs)', default=6.0)
    yuca_weight = fields.Float(string='Peso de Yuca (lbs)', default=6.0)
    
    def action_discard_batch(self):
        self.ensure_one()
        if self.state in ['done', 'cancel']:
            return
            
        # Cancel all work orders
        self.workorder_ids.write({'state': 'cancel'})
        
        # Cancel all stock moves
        (self.move_raw_ids | self.move_finished_ids).write({'state': 'cancel'})
        
        # Mark MO as cancelled with full waste
        self.write({
            'state': 'cancel',
            'merma_verif': self.product_qty,
        })
        
    workorder_count = fields.Integer(compute='_compute_workorder_count', string='Work Order Count')

    @api.depends('workorder_ids')
    def _compute_workorder_count(self):
        for production in self:
            production.workorder_count = len(production.workorder_ids)

    def action_view_workorders(self):
        self.ensure_one()
        return {
            'name': 'Work Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'mrp.workorder',
            'view_id': self.env.ref('kani_produccion.mrp_workorder_report_tree_view').id,
            'domain': [('production_id', '=', self.id)],
            'target': 'new',
        }

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    def button_pending(self):
        return self.write({'state': 'pending'})

    def _should_record_production(self):
        return True