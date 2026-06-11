# GitLab Project Management for Odoo 18

Integrate your Odoo Project Management with GitLab.com. Track commits, branches, and documentation progress across multiple repositories directly from your Odoo instance.

## Features

- **Multi-Repository Support**: Link multiple GitLab repositories to a single Odoo project.
- **Commit Timeline**: View a full history of commits within each Odoo project.
- **Real-time Sync**: Automatic updates using GitLab Webhooks.
- **Scheduled Sync**: Periodic background syncing via Odoo Scheduled Actions.
- **Documentation Progress**: Track and visualize documentation progress for each project.
- **Easy Configuration**: Simple setup for GitLab Cloud (GitLab.com) or self-hosted instances.

## Installation

1. Copy the `gitlab_project_management` folder to your Odoo custom addons directory.
2. Restart your Odoo server.
3. Enable developer mode.
4. Go to **Apps** and click **Update Apps List**.
5. Search for "GitLab Project Management" and click **Activate**.

## Configuration

### 1. GitLab Personal Access Token
1. Go to your GitLab account settings.
2. Navigate to **Access Tokens**.
3. Create a new token with `read_api` scope.
4. Copy the token.

### 2. Odoo Setup
1. In Odoo, go to **Project > Configuration > GitLab Integration > GitLab Instances**.
2. Create a new instance:
   - **Name**: e.g., GitLab Cloud
   - **Base URL**: `https://gitlab.com` (change if using self-hosted)
   - **Personal Access Token**: Paste your GitLab token.
3. Click **Test Connection**. Status should turn to "Active".

### 3. Link Repository to Project
1. Go to **Project > Configuration > GitLab Integration > Repositories**.
2. Create a new repository link:
   - **Name**: Your repo name.
   - **GitLab Project ID**: Found in GitLab project home page (e.g., `12345678`).
   - **Odoo Project**: Select the project you want to link.
3. Click **Sync Now** to pull initial data.

### 4. Webhook Setup (Real-time Updates)
1. In GitLab, go to your repository **Settings > Webhooks**.
2. Add a new webhook:
   - **URL**: `https://your-odoo-domain.com/gitlab/webhook`
   - **Trigger**: Push events.
   - **SSL verification**: Enabled.
3. Click **Add webhook**.

## Author
**Muhammad Ikhwan Fathulloh**
- [GitHub Profile](https://github.com/Muhammad-Ikhwan-Fathulloh)
- [Nocturnailed Community](https://github.com/Nocturnailed-Community)

## License
This module is licensed under the LGPL-3 License.
