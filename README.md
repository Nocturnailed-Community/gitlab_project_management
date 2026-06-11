# GitLab Project Management for Odoo 18

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple.svg)](https://www.odoo.com)

Modul Odoo 18 untuk integrasi dengan GitLab.com — kelola multi-repository, tracking commit, branch, dan progress dokumentasi langsung dari Odoo.

## ✨ Fitur Utama

| Fitur                 | Deskripsi                                                 |
| --------------------- | --------------------------------------------------------- |
| **Multi-Repository**  | Hubungkan beberapa repository GitLab ke satu project Odoo |
| **Commit Tracking**   | Lihat timeline commit langsung di project Odoo            |
| **Branch Tracking**   | Monitoring branch aktif beserta status protected          |
| **Webhook Real-time** | Otomatis sinkronisasi via GitLab webhook push event       |
| **Manual Sync**       | Tombol sinkronisasi manual per repository                 |
| **Doc Progress**      | Tracking progress dokumentasi per project (%)             |
| **Scheduled Sync**    | Cron job untuk sinkronisasi otomatis harian               |

## 📋 Persyaratan

- **Odoo 18** (Community atau Enterprise)
- **Python 3.10+**
- **Library Python**: `requests` (biasanya sudah terinstal di Odoo)
- **GitLab.com** Personal Access Token dengan scope `read_api` dan `read_repository`

## 🚀 Instalasi

> **⚠️ PENTING**: Modul ini **TIDAK BISA** diinstal via "Import Module" (upload ZIP) di web interface Odoo, karena modul ini mendefinisikan model Python baru yang memerlukan restart Odoo registry. Modul harus diinstal langsung di server.

### Langkah 1: Clone Repository

```bash
cd /opt/odoo/custom-addons/
# atau di path addons custom Anda
git clone https://github.com/Nocturnailed-Community/OdooGitlabProjectManagement.git
```

### Langkah 2: Pindahkan Folder Module

```bash
# Pastikan folder module berada langsung di addons path
mv OdooGitlabProjectManagement/gitlab_project_management /opt/odoo/custom-addons/gitlab_project_management

# Hapus folder wrapper jika tidak diperlukan
rm -rf OdooGitlabProjectManagement
```

### Langkah 3: Pastikan Addons Path Terdaftar

Edit file konfigurasi Odoo (`/etc/odoo/odoo.conf` atau sejenisnya):

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/opt/odoo/custom-addons
```

Pastikan path `/opt/odoo/custom-addons` (atau path yang Anda gunakan) sudah terdaftar di `addons_path`.

### Langkah 4: Restart Odoo

```bash
sudo systemctl restart odoo
```

### Langkah 5: Install Module di Odoo

1. Login ke Odoo sebagai Administrator
2. Aktifkan **Developer Mode**: Settings → Developer Tools → Activate Developer Mode
3. Klik **Apps** → **Update Apps List** → **Update**
4. Cari `GitLab Project Management` di daftar Apps
5. Klik **Activate** / **Install**

## ⚙️ Konfigurasi

### 1. Membuat GitLab Instance

1. Buka menu **Project** → **GitLab** → **Instances**
2. Klik **Create**
3. Isi field:
   - **Name**: Nama koneksi (misal: "GitLab.com")
   - **Base URL**: `https://gitlab.com` (default)
   - **Personal Access Token**: Token dari GitLab Anda
4. Klik **Test Connection** untuk memverifikasi

#### Cara Membuat Personal Access Token di GitLab:
1. Login ke [gitlab.com](https://gitlab.com)
2. Klik avatar → **Preferences** → **Access Tokens**
3. Buat token baru dengan scope:
   - ✅ `read_api`
   - ✅ `read_repository`
4. Copy token yang dihasilkan

### 2. Menghubungkan Repository ke Project

1. Buka menu **Project** → **GitLab** → **Repositories**
2. Klik **Create**
3. Isi field:
   - **Repository Name**: Nama repository
   - **GitLab Project ID**: ID angka dari project GitLab (lihat di Settings → General)
   - **GitLab Instance**: Pilih instance yang telah dibuat
   - **Odoo Project**: Pilih project Odoo yang akan dihubungkan
4. Klik **Sync Now** untuk sinkronisasi awal

### 3. Setup Webhook (Opsional - untuk Real-time Sync)

1. Di GitLab, buka repository → **Settings** → **Webhooks**
2. Tambahkan webhook baru:
   - **URL**: `https://your-odoo-domain.com/gitlab/webhook`
   - **Secret Token**: (kosongkan)
   - **Trigger**: ✅ Push events
   - **SSL verification**: ✅ Enable
3. Klik **Add webhook**

Setiap push ke repository akan otomatis mencatat commit baru di Odoo.

## 📖 Cara Penggunaan

### Melihat Commit di Project

1. Buka **Project** yang sudah dihubungkan dengan repository
2. Di form project, klik tombol **Commits** untuk melihat semua commit terkait
3. Commit ditampilkan dalam urutan terbaru

### Sinkronisasi Manual

1. Buka **Project** → **GitLab** → **Repositories**
2. Pilih repository yang ingin di-sync
3. Klik tombol **Sync Now**
4. Branch dan commit terbaru akan ter-update

### Sinkronisasi Otomatis (Cron)

Modul ini menyediakan scheduled action yang berjalan otomatis setiap hari untuk menyinkronkan semua repository yang aktif. Cron job dapat dikonfigurasi di:
- **Settings** → **Technical** → **Scheduled Actions** → **GitLab: Auto Sync Repositories**

### Tracking Progress Dokumentasi

1. Buka project yang terhubung
2. Update field **Doc Progress (%)** secara manual untuk tracking progress dokumentasi
3. Nilai progress ditampilkan di kanban view project

## 🏗️ Struktur Module

```
gitlab_project_management/
├── __init__.py                  # Root imports
├── __manifest__.py              # Module metadata & dependencies
├── models/
│   └── __init__.py              # Semua model definitions
│       ├── GitLabInstance       # Koneksi ke GitLab (URL + Token)
│       ├── GitLabRepository     # Link repository ke project
│       ├── GitLabBranch         # Data branch per repository
│       ├── GitLabCommit         # Data commit per repository
│       └── ProjectProject       # Inherit project.project
├── controllers/
│   └── __init__.py              # Webhook controller (/gitlab/webhook)
├── views/
│   ├── gitlab_instance_views.xml
│   ├── gitlab_repository_views.xml
│   └── project_project_views.xml
├── security/
│   └── ir.model.access.csv     # Access rights (Project Manager)
├── data/
│   └── ir_cron.xml             # Scheduled action untuk auto sync
├── static/
│   └── description/            # Module icon & screenshots
├── LICENSE                     # LGPL-3 License
└── README.md                   # Dokumentasi ini
```

## 🔧 Model Database

### `gitlab.instance`
Menyimpan koneksi ke server GitLab.

| Field       | Tipe      | Deskripsi                                |
| ----------- | --------- | ---------------------------------------- |
| `name`      | Char      | Nama instance                            |
| `base_url`  | Char      | URL GitLab (default: https://gitlab.com) |
| `api_token` | Char      | Personal Access Token                    |
| `state`     | Selection | Status koneksi (draft/active/error)      |

### `gitlab.repository`
Menghubungkan repository GitLab ke project Odoo.

| Field               | Tipe     | Deskripsi                    |
| ------------------- | -------- | ---------------------------- |
| `name`              | Char     | Nama repository              |
| `gitlab_project_id` | Char     | ID project di GitLab         |
| `instance_id`       | Many2one | Referensi ke GitLab Instance |
| `project_id`        | Many2one | Referensi ke Odoo Project    |
| `last_sync_date`    | Datetime | Waktu sinkronisasi terakhir  |

### `gitlab.branch`
Data branch per repository.

| Field           | Tipe     | Deskripsi               |
| --------------- | -------- | ----------------------- |
| `name`          | Char     | Nama branch             |
| `repository_id` | Many2one | Referensi ke repository |
| `is_default`    | Boolean  | Apakah branch utama     |
| `protected`     | Boolean  | Status protected        |

### `gitlab.commit`
Data commit per repository.

| Field           | Tipe     | Deskripsi            |
| --------------- | -------- | -------------------- |
| `name`          | Char     | Hash commit          |
| `short_id`      | Char     | Short hash           |
| `title`         | Char     | Judul commit         |
| `message`       | Text     | Pesan commit lengkap |
| `author_name`   | Char     | Nama author          |
| `authored_date` | Datetime | Tanggal commit       |
| `web_url`       | Char     | Link ke GitLab       |

## 🔒 Hak Akses

Hak akses default diberikan kepada group **Project Manager** (`project.group_project_manager`):

| Model               | Read | Write | Create | Delete |
| ------------------- | ---- | ----- | ------ | ------ |
| `gitlab.instance`   | ✅    | ✅     | ✅      | ✅      |
| `gitlab.repository` | ✅    | ✅     | ✅      | ✅      |
| `gitlab.branch`     | ✅    | ✅     | ✅      | ✅      |
| `gitlab.commit`     | ✅    | ✅     | ✅      | ✅      |

## 🌐 Webhook API

### Endpoint
```
POST /gitlab/webhook
```

### Headers
```
Content-Type: application/json
X-Gitlab-Event: Push Hook
```

### Supported Events
- **Push Hook**: Mencatat commit baru secara otomatis

## ❓ Troubleshooting

### Module tidak muncul di daftar Apps
- Pastikan folder `gitlab_project_management` ada di salah satu path yang terdaftar di `addons_path`
- Restart Odoo: `sudo systemctl restart odoo`
- Update Apps List di menu Apps

### Error "model_gitlab_instance not found"
- Pastikan Anda **TIDAK** menginstal via "Import Module" (ZIP upload)
- Module ini harus diinstal via server addons path (lihat bagian Instalasi)

### Webhook tidak berfungsi
- Pastikan URL webhook bisa diakses dari internet
- Cek apakah `gitlab_project_id` di repository Odoo sesuai dengan ID project di GitLab
- Periksa Odoo log untuk error detail

### Test Connection gagal
- Pastikan Personal Access Token masih valid
- Pastikan token memiliki scope `read_api`
- Periksa koneksi internet server Odoo ke gitlab.com

## 👨‍💻 Kontributor

- **Muhammad Ikhwan Fathulloh** — Creator & Maintainer
  - GitHub: [@Muhammad-Ikhwan-Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)

## 📝 Lisensi

Module ini dilisensikan di bawah [LGPL-3.0](LICENSE).

---

> **Odoo Affiliate**: Gunakan Odoo untuk manajemen bisnis Anda — [Daftar di sini](https://www.odoo.com/r/aff-ikhwanfathulloh)
