
---

## 📦 BIM HUB Odoo (`bim_project`)

[![Build Status](https://img.shields.io/github/actions/workflow/status/as13af/BIM_HUB_ODOO/ci.yml?branch=main\&style=flat-square)](https://github.com/as13af/BIM_HUB_ODOO/actions)
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![PyPI Version](https://img.shields.io/pypi/v/odoo16-bim_project?style=flat-square)](https://pypi.org/project/odoo16-bim_project)
[![JWT Auth](https://img.shields.io/badge/JWT–enabled-green?style=flat-square)](https://jwt.io/)

A next‑generation **Common Data Environment (CDE)** for Odoo 16 CE that brings together **Building Information Modeling (BIM)**, **issue/document workflows**, **live Digital Twins**, and **JWT‑secured REST APIs**—all under one roof. Think **Catenda Hub** functionality built natively into your ERP.

---

## 🚀 Core Features

### 1. Centralized BIM Project Management

Define your projects with **IFC**, **BCF**, and **COBie** uploads, track budgets and stakeholders, and roll-up metrics via One2many relations—giving you a single source of truth for your entire AECOO lifecycle ([Wikipedia][1]).

### 2. BCF‑Style Issue Tracking

Create, assign, and resolve model‑linked issues with priorities, due dates, **viewpoint snapshots**, and threaded comments. Keep every clash or snag anchored to the exact model element—just like Catenda’s BCF server ([Catenda][2]).

### 3. Versioned Document Control

Store and version PDFs, DWGs, and images; enforce **draft→review→approved** workflows; classify documents via codes; and annotate them with **chatter‑style** comments. Maintain a complete audit trail for compliance and quality assurance ([Catenda][3]).

### 4. Live Digital Twin Integration

Host your **3D model files** alongside O\&M data, track **“last updated”** timestamps, and monitor issue‑resolution progress with real‑time metrics. Capture and browse historical **viewpoint snapshots** to support predictive maintenance—mirroring real‑world Digital Twin use cases ([Wikipedia][4]).

### 5. JWT‑Secured REST API Layer

Expose `/api/authenticate`, `/api/update/access-token`, `/api/update/refresh-token`, and `/api/revoke/token` endpoints to manage **access** and **refresh** tokens. Protect all custom routes with `auth="jwt_validator"`, enabling stateless, scalable integrations for mobile apps, IoT platforms, or custom front‑ends ([Wikipedia][5]).

---

## 🌐 Why Choose BIM HUB Odoo over Catenda Hub?

| Benefit                        | BIM HUB Odoo                            | Catenda Hub                       |
| ------------------------------ | --------------------------------------- | --------------------------------- |
| **Full ERP Integration**       | Projects ↔ Finance, Procurement, Assets | Requires separate ERP integration |
| **Zero Per‑User Fees**         | AGPL‑3.0, unlimited users               | SaaS, potential user‑based costs  |
| **Self‑Hosted Data Ownership** | Complete control & compliance           | Data stored in Catenda’s cloud    |
| **Unlimited Customization**    | Python‑based modules & Odoo App store   | Limited to built‑in workflows     |
| **Unified BI & Reporting**     | Odoo dashboards across all modules      | External BI tools needed          |

---

## ⚙️ Installation

1. **Clone** into your custom addons:

   ```bash
   git clone https://github.com/as13af/BIM_HUB_ODOO.git addons_custom/bim_project
   ```
2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Enable JWT Auth**:

   * Install the [`odoo_jwt`](https://apps.odoo.com/apps/modules/17.0/odoo_jwt) module.
4. **Restart** Odoo and update apps list.
5. **Install** **BIM HUB** from the Apps menu.

---

## 🔧 Configuration & Quick Start

1. **JWT Validator**

   * Go to **Settings → Technical → Authentication → JWT Validators**
   * Create a validator record (e.g. HS256 with your secret key).

2. **Project Setup**

   * Navigate to **BIM Hub Odoo → Projects → Manage Projects**
   * Create a new project, upload an IFC model, and invite stakeholders.

3. **Issue Workflow**

   * From within a project, click **Issues** → **Create**
   * Assign to a team member, capture a viewpoint snapshot, and comment.

4. **Document Approval**

   * Upload a document under **Documents**, click **Request Review**, then **Approve/Reject** via form buttons.

5. **Digital Twin Sync**

   * Upload a new model file under **Digital Twins**, click **Request Sync**, and monitor **Sync Progress**.

---

## 📚 Further Reading

* **Building Information Modeling**: An approach to manage digital representations of physical and functional asset characteristics ([Wikipedia][1]).
* **Digital Twin**: A live, bidirectional digital counterpart to a physical asset, enabling real‑time monitoring ([Wikipedia][4]).
* **Common Data Environment (CDE)**: Centralized project data platform for all stakeholders ([Catenda][2]).
* **JSON Web Token (JWT)**: Standard for stateless, compact authentication tokens ([Wikipedia][5]).

---

## 🤝 Contributing

All contributions are welcome!

1. **Fork** the repository on GitHub.
2. **Create** a feature branch (`git checkout -b feature/fooBar`).
3. **Commit** your changes (`git commit -am 'Add feature'`).
4. **Push** to the branch (`git push origin feature/fooBar`).
5. **Open** a Pull Request.

Please review our **Code of Conduct** and **Contribution Guidelines** in the `docs/` folder before you start. ([Delve AEC][6])

---

## 📜 License

This module is released under the **AGPL v3** license. See [LICENSE](LICENSE) for details.

---

Empower your Odoo to become a true **Common Data Environment**—no more silos, no more vendor lock‑in, just open standards and complete control.

[1]: https://en.wikipedia.org/wiki/Building_information_modeling?utm_source=chatgpt.com "Building information modeling - Wikipedia"
[2]: https://catenda.com/glossary/common-data-environment/?utm_source=chatgpt.com "CDE - Common Data Environment - Catenda"
[3]: https://catenda.com/bim-solutions-open-standards/catenda-hub-common-data-environment/?utm_source=chatgpt.com "Catenda Hub"
[4]: https://en.wikipedia.org/wiki/Category%3ABuilding_information_modeling?utm_source=chatgpt.com "Category:Building information modeling - Wikipedia"
[5]: https://en.wikipedia.org/wiki/JSON_Web_Token?utm_source=chatgpt.com "JSON Web Token"
[6]: https://delveaec.com/product/catenda-hub/?utm_source=chatgpt.com "Catenda Hub - Delve AEC"
