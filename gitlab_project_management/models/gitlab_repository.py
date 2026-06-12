# -*- coding: utf-8 -*-
from odoo import models, fields

class GitLabRepository(models.Model):
    _name = 'gitlab.repository'
    _description = 'GitLab Repository'

    name = fields.Char(string='Repository Name', required=True)
    gitlab_project_id = fields.Char(string='GitLab Project ID', help='Project ID or URL-encoded path')
    instance_id = fields.Many2one('gitlab.instance', string='GitLab Instance', required=True)
    project_id = fields.Many2one('project.project', string='Odoo Project', required=True)
    active = fields.Boolean(default=True)

    branch_ids = fields.One2many('gitlab.branch', 'repository_id', string='Branches')
    commit_ids = fields.One2many('gitlab.commit', 'repository_id', string='Commits')

    last_sync_date = fields.Datetime(string='Last Sync Date')

    def action_sync_now(self):
        import requests
        self.ensure_one()
        instance = self.instance_id
        headers = {'PRIVATE-TOKEN': instance.api_token}
        base_url = instance.base_url.rstrip('/')
        
        # 1. Sync Branches
        branch_url = f"{base_url}/api/v4/projects/{self.gitlab_project_id}/repository/branches"
        try:
            r = requests.get(branch_url, headers=headers, timeout=20)
            if r.status_code == 200:
                branches = r.json()
                for b in branches:
                    branch = self.env['gitlab.branch'].search([
                        ('name', '=', b['name']),
                        ('repository_id', '=', self.id)
                      ], limit=1)
                    if not branch:
                        branch = self.env['gitlab.branch'].create({
                            'name': b['name'],
                            'repository_id': self.id,
                        })
                    branch.write({
                        'is_default': b.get('default', False),
                        'protected': b.get('protected', False),
                    })
        except Exception:
            pass

        # 2. Sync Commits
        commit_url = f"{base_url}/api/v4/projects/{self.gitlab_project_id}/repository/commits"
        try:
            r = requests.get(commit_url, headers=headers, timeout=20)
            if r.status_code == 200:
                commits = r.json()
                for c in commits:
                    commit = self.env['gitlab.commit'].search([
                        ('name', '=', c['id']),
                        ('repository_id', '=', self.id)
                    ], limit=1)
                    if not commit:
                        self.env['gitlab.commit'].create({
                            'name': c['id'],
                            'short_id': c['short_id'],
                            'title': c['title'],
                            'message': c['message'],
                            'author_name': c['author_name'],
                            'author_email': c['author_email'],
                            'authored_date': c['authored_date'].replace('T', ' ').split('.')[0],
                            'web_url': c['web_url'],
                            'repository_id': self.id,
                        })
        except Exception:
            pass
        
        self.last_sync_date = fields.Datetime.now()
