from odoo import models, fields, api

class Service(models.Model):
    _name = 'res.service'
    _description = 'Servicios'

    name = fields.Char(required=True, string='Nombre')
    description = fields.Text(string='Descripción')
    price = fields.Float(required=True, string='Precio')
    duration = fields.Float(string='Duración (horas)')
    availability = fields.Selection([
        ('available', 'Disponible'),
        ('unavailable', 'No Disponible')],
        default='available',
        string='Disponibilidad'
    )


class Partner(models.Model):
    _inherit = 'res.partner'

    is_vip = fields.Boolean(string='Cliente VIP', default=False)
    booking_history = fields.One2many('res.booking', 'client_id', string='Historial de Reservas')


class Booking(models.Model):
    _name = 'res.booking'
    _description = 'Reservas'

    client_id = fields.Many2one('res.partner', string='Cliente', required=True)
    service_id = fields.Many2one('res.service', string='Servicio', required=True)
    booking_datetime = fields.Datetime(string='Fecha/Hora', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('canceled', 'Cancelado')],
        default='draft',
        string='Estado'
    )
    calculated_price = fields.Float(string='Precio Calculado', compute='_compute_calculated_price', store=True)

    @api.depends('service_id.price', 'client_id.is_vip')
    def _compute_calculated_price(self):
        for record in self:
            base_price = record.service_id.price
            if record.client_id.is_vip:
                record.calculated_price = base_price * 0.9
            else:
                record.calculated_price = base_price

    @api.model
    def create(self, vals):
        booking = super(Booking, self).create(vals)
        if booking.state == 'confirmed':
            self.create_invoice(booking)
        return booking

    def create_invoice(self, booking):
        invoice_vals = {
            'partner_id': booking.client_id.id,
            'amount_total': booking.calculated_price,
            'booking_id': booking.id,
        }
        self.env['account.move'].create(invoice_vals)
