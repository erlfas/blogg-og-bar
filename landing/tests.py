from django.test import TestCase, Client
from django.urls import reverse
from .models import ShowcaseApp


class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_status_code(self):
        """Verify the root landing page returns 200 OK."""
        response = self.client.get(reverse('landing:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/index.html')
        self.assertTemplateUsed(response, 'landing/base.html')

    def test_landing_page_content_and_links(self):
        """Verify key branding and links to simpleplanner.blottogbar.no exist."""
        response = self.client.get(reverse('landing:index'))
        self.assertContains(response, 'blott og bar')
        self.assertContains(response, 'Simple Planner')
        self.assertContains(response, 'https://simpleplanner.blottogbar.no')

    def test_health_check(self):
        """Verify the health check endpoint returns JSON ok."""
        response = self.client.get(reverse('landing:health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok', 'app': 'blottogbar-landing'})

    def test_showcase_app_model(self):
        """Verify database model creation and string representation."""
        app = ShowcaseApp.objects.create(
            title='Test App',
            slug='test-app',
            tagline='A simple test tool',
            description='Detailed test description',
            url='https://test.blottogbar.no',
            status='live',
            badge_label='Test Live'
        )
        self.assertEqual(str(app), 'Test App (Live in Production)')
        
        # When model exists, it shows in context
        response = self.client.get(reverse('landing:index'))
        self.assertContains(response, 'Test App')
        self.assertContains(response, 'https://test.blottogbar.no')
