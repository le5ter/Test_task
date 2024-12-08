def init_app(app, **kwargs):
    from importlib import import_module

    for module_name in ("admin", "api", "transaction"):
        import_module('.%s' % module_name, package=__name__).init_app(app, **kwargs)
