{
    'name': 'BIM HUB Odoo',
    # 'name': 'ASTIL SAMA - c:\Users\PC\Downloads\wmremove-transformed (1).png ',
    'version': '1.0',
    'depends': [
        'base',
        'sale',
        'stock',
        'project',
        'hr',
        'mrp',
        'web',
        'contacts',
        'uom',  # Add this line to depend on the uom module
    ],
    'author': 'Ali Shidqie Al Faruqi',
    'data': [
        # 'views/digital_twin/digital_twin_views.xml',
        # 'views/document/document_views.xml',
        # 'views/document/document_comment_views.xml',
        # 'views/issue/issue_views.xml',
        # 'views/issue/issue_comment_views.xml',
        'views/project/project_views.xml',
        
        # 'views/bim_change_log_views.xml',
        # 'views/bim_cost_estimate_views.xml',
        # 'views/bim_element_views.xml',
        # 'views/bim_model_views.xml',
        # 'views/bim_inspection_views.xml',
        # 'views/bim_material_views.xml',
        # 'views/bim_project_views.xml',
        # 'views/bim_task_views.xml',
        # 'views/js_template_views.xml',

    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'bim_project/static/src/components/**/*.js',  # ✅ All JS files in "components" & subfolders
            'bim_project/static/src/components/**/*.xml', # ✅ All XML files in "components" & subfolders
            'bim_project/static/src/components/**/*.scss' # ✅ All SCSS files in "components" & subfolders
        ],
    },
}
