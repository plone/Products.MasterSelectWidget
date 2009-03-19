from StringIO import StringIO

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin

from Products.MasterSelectWidget.config import *

def install(self):
    out = StringIO()

    if INSTALL_DEMO_TYPE:
        installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)

    install_subskin(self, out, GLOBALS)
    out.write("Successfully installed %s." % PROJECTNAME)
    return out.getvalue()
