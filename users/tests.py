import json

from django.conf import settings
from django.core import mail

from django.test import TestCase
from django.utils import timezone

from users.models import User


class UsersTests(TestCase):
    def setUp(self):
        self.password = 'secret'
        self.su = User.objects.create_superuser(email='super@user.com',
                                                password=self.password)

        now = timezone.now()
        self.u1 = User.objects.create_user(email='user1@user.com')

    def login(self, user):
        self.client.login(email=user.email, password=self.password)

    def test_user_detail(self):
        url = self.u1.get_absolute_url()

        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 302)

        self.login(self.su)
        resp = self.client.get(url)
        self.assertContains(resp, self.u1.email)

        resp = self.client.post(url)
        self.assertEquals(resp.status_code, 400)

        resp = self.client.post(url, {
            'content': 'xyzzy',
        })
        self.assertEquals(resp.status_code, 200)
        d = json.loads(resp.content.decode('utf8'))
        self.assertIn('result', d)
        self.assertRegex(d['result'], 'id="note-\d+"')

        self.assertEquals(len(mail.outbox), len(settings.MANAGERS))
        # print(msg.message().as_bytes().decode('utf8'))
        mail.outbox = []

        resp = self.client.post(url, {
            'content': 'xyzzy',
            'send_to_user': '1',
        })
        self.assertEquals(resp.status_code, 200)
        d = json.loads(resp.content.decode('utf8'))
        self.assertIn('result', d)
        self.assertRegex(d['result'], 'id="note-\d+"')

        self.assertEquals(len(mail.outbox), len(settings.MANAGERS) + 1)
