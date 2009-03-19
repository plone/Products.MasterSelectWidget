try:
    from Products.CMFCore.permissions import AddPortalContent
except ImportError:
    from Products.CMFCore.CMFCorePermissions import AddPortalContent

PROJECTNAME = 'MasterSelectWidget'
SKINS_DIR = 'skins'
GLOBALS = globals()

ADD_CONTENT_PERMISSION = AddPortalContent

INSTALL_DEMO_TYPE = True
