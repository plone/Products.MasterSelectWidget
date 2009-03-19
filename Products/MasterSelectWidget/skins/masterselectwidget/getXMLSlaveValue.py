## Script (Python) "getXMLValue"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=method,param,value
##title=Get a value from XML request

from Products.CMFCore.utils import getToolByName

params = {param:value}
result = getattr(context, method)(**params)

utils = getToolByName(context, 'plone_utils')
charset = utils.getSiteEncoding()

RESPONSE = context.REQUEST.RESPONSE
RESPONSE.setHeader('Content-Type', 'text/xml; charset=%s' % charset)

# XXX escape special characters

return "%s" % context.translate(result)
