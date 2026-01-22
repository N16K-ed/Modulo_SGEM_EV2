from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


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
    # Es buena práctica poner inverse_name en One2many
    booking_history = fields.One2many('res.booking', 'client_id', string='Historial de Reservas')


class Booking(models.Model):
    _name = 'res.booking'
    _description = 'Reservas'

    client_id = fields.Many2one('res.partner', string='Cliente', required=True)
    service_id = fields.Many2one('res.service', string='Servicio', required=True)
    booking_datetime = fields.Datetime(string='Fecha/Hora', required=True, default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('canceled', 'Cancelado')],
        default='draft',
        string='Estado'
    )
    calculated_price = fields.Float(string='Precio Calculado', compute='_compute_calculated_price', store=True)

    # Campo para relacionar con la factura creada
    invoice_id = fields.Many2one('account.move', string='Factura', readonly=True)

    @api.depends('service_id.price', 'client_id.is_vip')
    def _compute_calculated_price(self):
        for record in self:
            base_price = record.service_id.price if record.service_id else 0.0
            if record.client_id.is_vip:
                record.calculated_price = base_price * 0.9  # 10% descuento
            else:
                record.calculated_price = base_price


    # OBJETIVO SEMANA 2: Validaciones

    @api.constrains('booking_datetime')
    def _check_date(self):
        for record in self:
            if record.booking_datetime and record.booking_datetime < fields.Datetime.now():
                raise ValidationError("No puedes crear reservas en fechas pasadas.")

    @api.constrains('service_id')
    def _check_service_availability(self):
        for record in self:
            if record.service_id.availability == 'unavailable':
                raise ValidationError("El servicio seleccionado no está disponible actualmente.")


    # OBJETIVO SEMANA 2: Acciones y Facturación


    def action_confirm(self):
        """ Cambia estado a confirmado y crea factura """
        for record in self:
            if record.state == 'canceled':
                raise ValidationError("No puedes confirmar una reserva cancelada.")

            record.write({'state': 'confirmed'})
            if not record.invoice_id:  # Evitar duplicar facturas
                record._create_invoice()

    def action_cancel(self):
        """ Cambia estado a cancelado """
        for record in self:
            if record.state == 'confirmed' and record.invoice_id:
                raise ValidationError("La reserva ya está facturada, no se puede cancelar directamente.")
            record.write({'state': 'canceled'})

    def _create_invoice(self):
        """ Lógica interna para crear la factura en Account """
        invoice_vals = {
            'partner_id': self.client_id.id,
            'move_type': 'out_invoice',  # Factura de cliente
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f"Reserva: {self.service_id.name}",
                'quantity': 1,
                'price_unit': self.calculated_price,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id


    # OBJETIVO SEMANA 2: Cron Job (Cancelación automática)

    @api.model
    def _cron_cancel_expired_bookings(self):
        # Buscar reservas en borrador creadas hace más de 24 horas
        # Para probar se puede usar time_limit = fields.Datetime.now() - timedelta(minutes=1)
        time_limit = fields.Datetime.now() - timedelta(hours=24)
        expired_bookings = self.search([
            ('state', '=', 'draft'),
            ('create_date', '<', time_limit)
        ])
        for booking in expired_bookings:
            booking.write({'state': 'canceled'})