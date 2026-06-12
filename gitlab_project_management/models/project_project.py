# -*- coding: utf-8 -*-
from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    gitlab_repository_ids = fields.One2many('gitlab.repository', 'project_id', string='GitLab Repositories')
    gitlab_commit_count = fields.Integer(compute='_compute_gitlab_stats')
    doc_progress = fields.Float(string='Doc Progress (%)', default=0.0)

    def _compute_gitlab_stats(self):
        for project in self:
            project.gitlab_commit_count = self.env['gitlab.commit'].search_count([('project_id', '=', project.id)])

    def action_view_gitlab_commits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'GitLab Commits',
            'res_model': 'gitlab.commit',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }
