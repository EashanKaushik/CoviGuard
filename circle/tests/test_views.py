from django.test import TestCase, Client
from django.urls import reverse
from circle.models import Circle, CircleUser, RecentCircle, Policy, RequestCircle
from login.models import UserData
import datetime


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.session = self.client.session
        self.session[
            "user_key"
        ] = "IkVhc2hhbkthdXNoaWsi:1nYapk:h76qaIXuhZkcmoL0DPN_lCrB_88Cs2ezsLn1vMXe0cY"
        self.session.save()

        self.dashboard_url = reverse(
            "circle:dashboard",
            args=["EashanKaushik"],
        )

        self.user_circle_url = reverse(
            "circle:user_circle",
            args=["EashanKaushik", "1"],
        )

        self.create_url = reverse(
            "circle:create",
        )

        self.notify_url = reverse("circle:notify")

        self.exitcircle = reverse("circle:exitcircle", args=["EashanKaushik", "1"])

        self.deletecircle = reverse("circle:deletecircle", args=["EashanKaushik", "1"])

        self.userdata = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="EashanKaushik",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.userdata_2 = UserData.objects.create(
            firstname="Chinmay",
            lastname="Kulkarni",
            password="coviguard",
            username="ChinmayKulkarni",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.userdata_3 = UserData.objects.create(
            firstname="Srijan",
            lastname="Malhotra",
            password="coviguard",
            username="SrijanMalhotra",
            email="test@gmail.com",
            dob=datetime.datetime.now(),
            work_address="1122",
            home_adress="1122",
        )

        self.recentcircle = RecentCircle.objects.create(
            username=self.userdata, recent_circle="[1]"
        )

        self.circle = Circle.objects.create(
            circle_id=1,
            circle_name="TestCircle",
            admin_username=self.userdata,
            no_of_users=2,
        )
        self.circle_user_data = CircleUser.objects.create(
            circle_id=self.circle, username=self.userdata, is_admin=True, is_member=True
        )

        self.circle_user_data_2 = CircleUser.objects.create(
            circle_id=self.circle,
            username=self.userdata_2,
            is_admin=False,
            is_member=True,
        )

        self.policy = Policy.objects.create(
            policy_id=1,
            policy_name="TestPolicy",
            policy_desc="TestPolicyDesc",
            policy_level=0,
        )

        self.request_circle = RequestCircle.objects.create(
            request_id=1, circle_id=self.circle, username=self.userdata_3
        )

    def test_circle(self):
        response = self.client.get(self.dashboard_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/circle.html")

        response = self.client.get(self.user_circle_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/current-circle.html")

        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/add.html")

        response = self.client.get(self.exitcircle)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/circle.html")

        response = self.client.get(self.deletecircle)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/circle.html")

    def test_current_circle(self):
        response = self.client.post(
            self.user_circle_url, data={"remove_user": "ChinmayKulkarni"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/current-circle.html")

    def test_request_circle(self):
        response = self.client.post(self.create_url, data={"request_circle": ""})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/add.html")

    def test_create_circle(self):
        response = self.client.post(
            self.create_url,
            data={"create_circle": "", "circle_name": "TestCircle_2", "policy_id": "1"},
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/add.html")

    def test_create_circle_withSameName(self):
        response = self.client.post(
            self.create_url,
            data={"create_circle": "", "circle_name": "TestCircle", "policy_id": "1"},
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/add.html")

    def test_notify_accept(self):
        response = self.client.post(self.notify_url, data={"accept_circle": 1})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/notifications.html")

    def test_notify_reject(self):
        response = self.client.post(self.notify_url, data={"reject_circle": 1})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "circle/notifications.html")
