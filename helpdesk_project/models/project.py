from odoo import models, api, fields, _
import logging
_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    ticket_ids = fields.One2many(
    comodel_name='helpdesk.ticket',
    inverse_name='task_id',
    string='Tickets'
    )
    ticket_count = fields.Integer(
        compute='_compute_ticket_count',
        string="Number of Tickets"
    )

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for task in self:
            task.ticket_count=len(task.ticket_ids)


    def action_new_ticket(self):
        action = self.env.ref("helpdesk_project.task_action_ticket_new").read()[0]
        action['context'] = {
            'default_task_id': self.id,
            'default_project_id': self.project_id and self.project_id.id,
        }
        _logger.info("Action del ticket------------------------------------------------------------")
        _logger.info(action)
        return action

    def action_view_tickets(self):
        action = {
            "name": self.name,
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "helpdesk.ticket",
            "type": "ir.actions.act_window",
            "domain": [("task_id", "child_of", self.id)],
            "context": self.env.context,
        }
        return action
