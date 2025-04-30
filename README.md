# BIM_HUB_ODOO
## 📦 BIM Project (bim_project)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/bim_project/actions)  
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)  
[![PyPI Version](https://img.shields.io/pypi/v/odoo16-bim_project)](https://pypi.org/project/odoo16-bim_project)  
[![Quality Gate](https://img.shields.io/codecov/c/github/yourusername/bim_project)](https://codecov.io/github/yourusername/bim_project)  

A powerful Odoo 16 CE module that brings **Building Information Modeling (BIM)**, a **Common Data Environment (CDE)**, and **JWT-secured API** into your ERP—fully inspired by [Catenda Hub](https://catenda.com) and open standards.

---

## 🚀 Features

- **Project Management** (`bim.project`)  
  Create and manage BIM projects with metadata, stakeholders, and file uploads (IFC, BCF, COBie).

- **Issue Tracking** (`bim.issue`, `bim.issue.comment`)  
  BCF-style issues with statuses, priorities, snapshots, and threaded comments.

- **Document Control** (`bim.document`, `bim.document.comment`)  
  Versioned document library (IFC, DWG, PDF, images) with classification codes and collaborative annotations.

- **Digital Twin** (`bim.digital.twin`)  
  Live digital replicas with status updates, last-updated timestamps, and integrated issue workflows.

- **JWT-Secured REST API** (`auth_jwt`)  
  - **Authenticate**: Obtain access & refresh tokens via `/api/authenticate`.  
  - **Protected Endpoints**: All custom endpoints require `Authorization: Bearer <token>`.  
  - **Token Refresh & Revoke**: `/api/update/access-token`, `/api/update/refresh-token`, `/api/revoke/token`.  
  - Enables secure mobile or external integrations without session cookies.

- **Open Standards & Integrations**  
  Use IFC, BCF, COBie, and Catenda Boost-style REST APIs for seamless data exchange.

---

## 🛠️ Installation

1. **Clone** this repo into your custom addons folder:  
   ```bash
   git clone https://github.com/yourusername/bim_project.git /path/to/odoo/addons_custom/bim_project
