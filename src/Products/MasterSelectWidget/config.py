try:
    from Products.CMFCore.permissions import AddPortalContent
except ImportError:
    from Products.CMFCore.CMFCorePermissions import AddPortalContent

PROJECTNAME = 'MasterSelectWidget'
GLOBALS = globals()

ADD_CONTENT_PERMISSION = AddPortalContent
