# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError

class AllocateResourceWizard(models.TransientModel):
    _name = "allocate.resource.wizard"
    
    date_start = fields.Datetime(string="Date Start", required=True)
    date_end = fields.Datetime(string="Date end", required=True)
    resources = fields.Many2many('resource.resource', string="Resources")
    allocation_type = fields.Selection([('booked','Book'),
                                       ('option','Option')],
                                       string="Allocation type", required=True)
    resource_type = fields.Selection([('resource','Resource'),
                                      ('category','Category')],
                                      string="Allocate on", default="resource", required=True)
    resource_category_id = fields.Many2one('resource.category', string="Resource Category")
    checked_resources = fields.Boolean(string="Checked ressources")
    partner_id = fields.Many2one('res.partner', string="Allocate to", required=True)
    date_lock = fields.Date(string="Date lock")

    @api.model
    def default_get(self, fields):
        result = super(AllocateResourceWizard, self).default_get(fields)
        result['resources'] = self._context.get('active_ids',False)
         
        return result
    
    @api.onchange('resource_category_id')
    def onchange_resource_category(self):
        if self.checked_resources and self.resource_category_id:
            self.checked_resources = False
    
    @api.onchange('date_start','date_end')
    def onchange_dates(self):
        if self.checked_resources and self.date_start and self.date_end:
            self.checked_resources = False
            
    @api.onchange('checked_resources')
    def onchange_checked_resources(self):
        if self.checked_resources and self.date_start and self.date_end:
            self.checked_resources = True
            self.search_resource()

    @api.model
    def search_resource(self):
        resource_obj = self.env['resource.resource']
        res = []
        if self.resource_type == 'resource':
            res = self.resources.check_availabilities(self.date_start, self.date_end)
        else:
            res = self.resource_category_id.resources.check_availabilities(self.date_start, self.date_end)
        if res:
            self.resources = resource_obj.browse(res)
        else:
            self.resources = None
        
    @api.multi
    def book_resource(self):
        if self.resources:
            self.resources.allocate_resource(self.allocation_type, self.date_start, self.date_end, self.partner_id, self.date_lock)
