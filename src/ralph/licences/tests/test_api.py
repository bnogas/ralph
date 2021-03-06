# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import status

from ralph.api.tests._base import RalphAPITestCase
from ralph.back_office.tests.factories import BackOfficeAssetFactory
from ralph.licences.models import BaseObjectLicence, Licence, LicenceUser
from ralph.licences.tests.factories import LicenceFactory


class LicenceAPITests(RalphAPITestCase):
    def setUp(self):
        super().setUp()
        self.licence1, self.licence2 = LicenceFactory.create_batch(2)
        self.base_object = BackOfficeAssetFactory()
        LicenceUser.objects.create(licence=self.licence1, user=self.user1)
        BaseObjectLicence.objects.create(
            licence=self.licence2, base_object=self.base_object
        )

    def test_get_licence_list(self):
        url = reverse('licence-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Licence.objects.count())

    def test_get_licence_with_user_details(self):
        url = reverse('licence-detail', args=(self.licence1.id,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['number_bought'], self.licence1.number_bought
        )
        self.assertEqual(
            response.data['region']['id'], self.licence1.region.id
        )
        self.assertEqual(
            response.data['manufacturer']['id'], self.licence1.manufacturer.id
        )
        self.assertEqual(
            response.data['licence_type']['id'], self.licence1.licence_type.id
        )
        self.assertEqual(
            response.data['software']['id'], self.licence1.software.id
        )
        self.assertEqual(
            response.data['users'][0]['user']['id'], self.user1.id,
        )

    def test_get_licence_with_base_object_details(self):
        url = reverse('licence-detail', args=(self.licence2.id,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.data['base_objects'][0]['base_object'].endswith(
                reverse('baseobject-detail', args=(self.base_object.id,))
            )
        )
