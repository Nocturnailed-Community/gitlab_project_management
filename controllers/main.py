# -*- coding: utf-8 -*-
import json
import logging
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)

class GitLabWebhookController(http.Controller):

    @http.route('/gitlab/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def gitlab_webhook(self, **post):
        data = request.get_json_data()
        event_type = request.httprequest.headers.get('X-Gitlab-Event')
        
        if not data or not event_type:
            return {'status': 'error', 'message': 'No data'}

        project_id = data.get('project', {}).get('id')
        if not project_id:
            return {'status': 'error', 'message': 'Project ID missing'}

        # Find repository
        repo = request.env['gitlab.repository'].sudo().search([
            ('gitlab_project_id', '=', str(project_id))
        ], limit=1)

        if not repo:
            _logger.warning("Received webhook for unknown GitLab project ID: %s", project_id)
            return {'status': 'ignored'}

        if event_type == 'Push Hook':
            self._handle_push_event(repo, data)
        
        return {'status': 'success'}

    def _handle_push_event(self, repo, data):
        commits = data.get('commits', [])
        for c in commits:
            commit = request.env['gitlab.commit'].sudo().search([
                ('name', '=', c['id']),
                ('repository_id', '=', repo.id)
            ], limit=1)
            if not commit:
                request.env['gitlab.commit'].sudo().create({
                    'name': c['id'],
                    'short_id': c['id'][:8],
                    'title': c['message'].split('\n')[0],
                    'message': c['message'],
                    'author_name': c['author']['name'],
                    'author_email': c['author']['email'],
                    'authored_date': c['timestamp'].replace('T', ' ').split('+')[0],
                    'web_url': c['url'],
                    'repository_id': repo.id,
                })
        repo.sudo().last_sync_date = fields.Datetime.now()
