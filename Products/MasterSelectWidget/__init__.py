from Products.CMFCore.utils import ContentInit
from Products.Archetypes.public import process_types, listTypes
from Products.MasterSelectWidget.config import *

def initialize(context):
    import MasterSelectDemo

    content_types, constructors, ftis=process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
