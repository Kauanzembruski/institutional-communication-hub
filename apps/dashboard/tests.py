from django.test import TestCase, override_settings


class AdminOnlyProjectTests(TestCase):
    @override_settings(
        SECRET_KEY="test-secret-key-only-for-automated-tests",
        SECURE_SSL_REDIRECT=False,
    )
    def test_root_has_no_public_template_view(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 404)

    @override_settings(
        SECRET_KEY="test-secret-key-only-for-automated-tests",
        SECURE_SSL_REDIRECT=False,
    )
    def test_admin_url_exists(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
