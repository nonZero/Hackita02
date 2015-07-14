from django.test import TestCase

from . import models
from projects.drive import id_from_url, retrieve_doc_content
from users.models import User


class DriveTests(TestCase):
    def test_retrieve(self):
        doc_id="186WhJNI4Z-2gU_lakB2kbuUC-lQ8zG9Nz9bK8sk3Ykg"
        d = retrieve_doc_content(doc_id)
        self.assertIn("123", d['title'])
        self.assertIn("123", d['text'])
        self.assertIn("<html", d['html'])

    def test_id_from_url(self):
        url = "https://docs.google.com/document/d/186WhJNI4Z-2gU_lakB2kbuUC-lQ8zG9Nz9bK8sk3Ykg/edit?usp=sharing"
        id = "186WhJNI4Z-2gU_lakB2kbuUC-lQ8zG9Nz9bK8sk3Ykg"
        self.assertEquals(id, id_from_url(url))

# class ProjectTests(TestCase):
#     def test_retrieve(self):
#         u = User.objects.create_user('x@y.z', 'xyzzy')
#         o = models.Project(
#             created_by=u,
#             title="foo",
#             summary="foo bar",
#             doc_id="186WhJNI4Z-2gU_lakB2kbuUC-lQ8zG9Nz9bK8sk3Ykg"
#         )
#         o.retrieve_content()
#         self.assertIn("123", o.content_text)
#         self.assertIn("<html", o.content_html)
#
#

# https://docs.google.com/document/d/186WhJNI4Z-2gU_lakB2kbuUC-lQ8zG9Nz9bK8sk3Ykg/edit?usp=sharing
