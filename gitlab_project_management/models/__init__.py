# -*- coding: utf-8 -*-
from odoo import models, fields, api

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

class GitLabBranch(models.Model):
    _name = 'gitlab.branch'
    _description = 'GitLab Branch'

    name = fields.Char(string='Branch Name', required=True)
    repository_id = fields.Many2one('gitlab.repository', string='Repository', required=True, ondelete='cascade')
    is_default = fields.Boolean(string='Is Default Branch')
    protected = fields.Boolean(string='Protected')
    last_commit_id = fields.Many2one('gitlab.commit', string='Last Commit')

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
