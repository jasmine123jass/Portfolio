from projects_app import views as _p_views

# Re-export certificate-related view callables expected by existing imports.
certificate_list = _p_views.certificate_list
certificate_create = getattr(_p_views, 'certificate_create', None)
certificate_update = getattr(_p_views, 'certificate_update', None)
certificate_delete = getattr(_p_views, 'certificate_delete', None)
