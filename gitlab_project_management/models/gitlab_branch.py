# -*- coding: utf-8 -*-
from odoo import models, fields

class GitLabBranch(models.Model):
    _name = 'gitlab.branch'
    _description = 'GitLab Branch'

    name = fields.Char(string='Branch Name', required=True)
    repository_id = fields.Many2one('gitlab.repository', string='Repository', required=True, ondelete='cascade')
    is_default = fields.Boolean(string='Is Default Branch')
    protected = fields.Boolean(string='Protected')
    last_commit_id = fields.Many2one('gitlab.commit', string='Last Commit')
