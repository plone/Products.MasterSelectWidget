# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from Products.MasterSelectWidget.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of Products.MasterSelectWidget into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if Products.MasterSelectWidget is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('Products.MasterSelectWidget'))

    def test_uninstall(self):
        """Test if Products.MasterSelectWidget is cleanly uninstalled."""
        self.installer.uninstallProducts(['Products.MasterSelectWidget'])
        self.assertFalse(self.installer.isProductInstalled('Products.MasterSelectWidget'))
