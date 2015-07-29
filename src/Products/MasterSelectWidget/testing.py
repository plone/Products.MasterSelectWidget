# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone import api

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from plone.testing import z2

import Products.MasterSelectWidget

import transaction

import unittest2 as unittest


class MasterSelectWidgetDemoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    products = ('Products.MasterSelectWidget',)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=Products.MasterSelectWidget, name='testing.zcml')
        for p in self.products:
            z2.installProduct(app, p)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'Products.MasterSelectWidget:demo')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        api.content.create(
            type='MasterSelectDemo',
            id='msw_demo',
            container=portal,
        )

        # Commit so that the test browser sees these objects
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            z2.uninstallProduct(app, p)


FIXTURE = MasterSelectWidgetDemoLayer(
    name="FIXTURE"
)


INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="INTEGRATION"
)


FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="FUNCTIONAL"
)


ACCEPTANCE = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="ACCEPTANCE"
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.demo = self.portal.msw_demo


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        self.demo = self.portal.msw_demo
