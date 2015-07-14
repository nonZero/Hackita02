from django.core.urlresolvers import reverse
from django.forms.utils import ErrorDict
from django.test import TestCase

from users.models import User, PersonalInfo


class RegiterTest(TestCase):
    def setUp(self):
        self.u_password = "foobar"
        self.u = User.objects.create_user("foo@bar.com",
                                          self.u_password)
        self.staff = User.objects.create_user("staff@bar.com", "staff")

    def test_personal_details(self):
        self.client.login(email=self.u.email, password=self.u_password)
        self.assertFalse(hasattr(self.u, 'personalinfo'))
        url = reverse('sa:personal_details')
        r = self.client.get(url)
        self.assertEquals(200, r.status_code)

        data = {
        }

        r = self.client.post(url, data)
        self.assertEquals(200, r.status_code)
        form = r.context['form']
        assert isinstance(form.errors, ErrorDict)
        self.assertNotEquals(len(form.errors), 0)

        data = {
            "hebrew_first_name": "פו",
            "hebrew_last_name": "בר",
            "english_first_name": "foo",
            "english_last_name": "bar",

            "main_phone": "050-5555555",
            "alt_phone": "050-7654321",

            "city": "Jerusalem",
            "address": "123 ACME St.",

            "gender": PersonalInfo.MALE,

            "skype_username": "kuku",
        }

        r = self.client.post(url, data)
        self.assertEquals(302, r.status_code)

        # self.u.refresh_from_db() # Does not work
        self.u = User.objects.get(id=self.u.id)

        for k, v in data.items():
            actual = getattr(self.u.personalinfo, k)
            self.assertEquals(actual, v)

        self.assertEquals(self.u.hebrew_display_name, "פו בר")
        self.assertEquals(self.u.english_display_name, "Foo Bar")

        # Filling personal details once is enough
        r = self.client.get(url)
        self.assertRedirects(r, reverse('sa:dashboard'))


        # def test_register(self):
        #     self.assertEquals(0, self.u.answers.count())
        #     self.client.login(email="foo@bar.com", password="foobar")
        #     r = self.client.get(reverse('register'))
        #     self.assertEquals(200, r.status_code)
        #
        #     r = self.client.post(reverse('register'))
        #     self.assertGreater(len(r.context['form'].errors), 0)
        #     self.assertEquals(200, r.status_code)
        #     self.assertEquals(0, self.u.answers.count())
        #
        #     data = {
        #             "english_first_name": "Udi",
        #             "alt_phone": "",
        #             "dob": "",
        #             "gender": u"\u05d6\u05db\u05e8",
        #             "skype": "",
        #             "hebrew_last_name": u"\u05d0\u05d5\u05e8\u05d5\u05df",
        #             "hebrew_first_name": u"\u05d0\u05d5\u05d3\u05d9",
        #             "address": "",
        #             "main_phone": "123123",
        #             "english_last_name": "Oron",
        #             "city": ""}
        #
        #     r = self.client.post(reverse('register'), data)
        #     self.assertEquals(302, r.status_code)
        #     self.assertEquals(1, self.u.answers.count())
        #
        # def test_tagging(self):
        #
        #     cool = Tag.objects.create(name="Cool", group=TagGroup.SILVER)
        #     yuck = Tag.objects.create(name="Yuck", group=TagGroup.NEGATIVE)
        #
        #     self.assertEquals(0, self.u.tags.count())
        #
        #     UserTag.objects.tag(self.u, cool, self.staff)
        #
        #     self.assertEquals(1, self.u.tags.count())
        #     self.assertEquals(1, self.u.logs.count())
        #
        #     UserTag.objects.tag(self.u, yuck, self.staff)
        #
        #     self.assertEquals(2, self.u.tags.count())
        #     self.assertEquals(2, self.u.logs.count())
        #
        #     UserTag.objects.tag(self.u, yuck, self.staff)
        #
        #     self.assertEquals(2, self.u.tags.count())
        #     self.assertEquals(2, self.u.logs.count())
        #
        #     UserTag.objects.untag(self.u, cool, self.staff)
        #
        #     self.assertEquals(1, self.u.tags.count())
        #     self.assertEquals(3, self.u.logs.count())
        #     UserTag.objects.untag(self.u, yuck, self.staff)
        #
        #     self.assertEquals(0, self.u.tags.count())
        #     self.assertEquals(4, self.u.logs.count())
        #
        #     UserTag.objects.untag(self.u, yuck, self.staff)
        #
        #     self.assertEquals(0, self.u.tags.count())
        #     self.assertEquals(4, self.u.logs.count())
