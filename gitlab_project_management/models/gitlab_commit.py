# -*- coding: utf-8 -*-
from odoo import models, fields

class GitLabCommit(models.Model):
    _name = 'gitlab.commit'
    _description = 'GitLab Commit'
    _order = 'authored_date desc'

    name = fields.Char(string='Commit Hash', required=True)
    short_id = fields.Char(string='Short ID')
    title = fields.Char(string='Title')
    message = fields.Text(string='Message')
    author_name = fields.Char(string='Author')
    author_email = fields.Char(string='Email')
    authored_date = fields.Datetime(string='Authored Date')
    web_url = fields.Char(string='Web URL')

    repository_id = fields.Many2one('gitlab.repository', string='Repository', required=True, ondelete='cascade')
    project_id = fields.Many2one('project.project', related='repository_id.project_id', store=True)
    task_id = fields.Many2one('project.task', string='Related Task')
