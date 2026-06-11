# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
_logger.info("Loading GitLab Instance model")

class GitLabInstance(models.Model):
    _name = 'gitlab.instance'
    _description = 'GitLab Instance'

    name = fields.Char(string='Name', required=True)
    base_url = fields.Char(string='Base URL', default='https://gitlab.com', required=True)
    api_token = fields.Char(string='Personal Access Token', required=True, password=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('error', 'Connection Error')
    ], default='draft')

    repository_ids = fields.One2many('gitlab.repository', 'instance_id', string='Repositories')

    def action_test_connection(self):
        import requests
        self.ensure_one()
        url = f"{self.base_url.rstrip('/')}/api/v4/user"
        headers = {'PRIVATE-TOKEN': self.api_token}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                self.state = 'active'
            else:
                self.state = 'error'
        except Exception:
            self.state = 'error'
