## 📦 BIM HUB Odoo (`bim_project`)

[![Build Status](https://img.shields.io/github/actions/workflow/status/as13af/BIM_HUB_ODOO/ci.yml?branch=main&style=flat-square)](https://github.com/as13af/BIM_HUB_ODOO/actions)  
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.en.html)  
[![PyPI Version](https://img.shields.io/pypi/v/odoo16-bim_project?style=flat-square)](https://pypi.org/project/odoo16-bim_project)  
[![JWT Auth](https://img.shields.io/badge/JWT–enabled-green?style=flat-square)](https://apps.odoo.com/apps/modules/17.0/odoo_jwt)  

A powerful Odoo 16 CE module that brings **BIM** (Building Information Modeling), a **CDE** (Common Data Environment), and **JWT-secured REST APIs** into your ERP—fully inspired by [Catenda Hub](https://catenda.com) .

## 🚀 Features

- **Project Management** (`bim.project`):  
  Centralized BIM project data (IFC/BCF/COBie uploads, stakeholders, budget) with One2many roll-ups .  
- **Issue Tracking** (`bim.issue`, `bim.issue.comment`):  
  BCF-style issues with statuses, priorities, snapshots, and threaded comments, replicating Catenda’s workflow .  
- **Document Control** (`bim.document`, `bim.document.comment`):  
  Versioned document library (PDF/DWG/images) with classification codes, approval status, and collaborative annotations .  
- **Digital Twin** (`bim.digital.twin`):  
  Live asset replicas with status, “last updated” timestamps, and integrated issue links for operations & maintenance .  
- **JWT-Secured REST API** (`auth_jwt`, `odoo_jwt`):  
  - **Authenticate** at `/api/authenticate` to receive access & refresh tokens :contentReference[oaicite:0]{index=0}.  
  - **Refresh/Revoke** tokens via `/api/update/access-token`, `/api/update/refresh-token`, and `/api/revoke/token` :contentReference[oaicite:1]{index=1}.  
  - **Protect** endpoints with `auth="jwt_validator"` attributes on routes :contentReference[oaicite:2]{index=2}.  

## 🛠️ Installation

1. **Clone** this repo into your custom addons folder:  
   ```bash
   git clone https://github.com/as13af/BIM_HUB_ODOO.git addons_custom/bim_project
