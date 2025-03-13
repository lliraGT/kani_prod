# models/production_control_wizard.py
from odoo import models, fields, api # type: ignore

class ProductionControlWizard(models.TransientModel):
    _name = 'production.control.wizard'
    _description = 'Production Control Wizard'

    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', required=True)
    
    cooking_temp = fields.Float(string='Temperatura de Cocción (°C)')
    weight_mp = fields.Integer(string='Minutos de pesado de materia prima')
    fridge_lbs = fields.Float(string='Libras entregadas a refrigerado')
    fridge_temp = fields.Float(string='Temperatura de alimento al ingresar a refrigerado (°C)')
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
    
    # Add ingredient weight fields to wizard
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

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self._context.get('active_id')
        if active_id:
            production = self.env['mrp.production'].browse(active_id)
            for field in fields_list:
                if hasattr(production, field):
                    res[field] = getattr(production, field)
        return res

    def action_confirm(self):
        self.ensure_one()
        production = self.production_id
        values = {}
        for field in self._fields:
            if field not in ['production_id', 'display_name', '__last_update', 'create_uid', 'create_date', 'write_uid', 'write_date']:
                values[field] = self[field]
        production.write(values)
        return {'type': 'ir.actions.act_window_close'}