# -*- coding: utf-8 -*-
{
    'name': 'GitLab Project Management',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Integrate Odoo Projects with GitLab repositories',
    'description': """
        Track GitLab commits, branches, and documentation progress directly from Odoo projects.
        Features:
        - Multi-repository support
        - Commit timeline in projects
        - Branch tracking
        - Webhook integration
        - Documentation progress dashboard
    """,
    'author': 'Muhammad Ikhwan Fathulloh',
    'website': 'https://github.com/Muhammad-Ikhwan-Fathulloh',
    'depends': ['base', 'project', 'base_setup'],
    'data': [
        'security/ir.model.access.xml',
        'views/gitlab_instance_views.xml',
        'views/gitlab_repository_views.xml',
        'views/project_project_views.xml',
        'data/ir_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
