from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    force_email_send = fields.Boolean(string="Force mail send?")

    def send_mail(
        self,
        res_id,
        force_send=False,
        raise_exception=False,
        email_values=None,
        email_layout_xmlid=False,
    ):
        return super(MailTemplate, self).send_mail(
            res_id,
            force_send=self.force_email_send,
            raise_exception=raise_exception,
            email_values=email_values,
            email_layout_xmlid=email_layout_xmlid,
        )
