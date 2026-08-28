import json
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

    def test_landing_page_showcase_apps(self):
        """Verify that all three sub-apps are showcased with their URLs."""
        response = self.client.get(reverse('landing:index'))
        # Simple Planner
        self.assertContains(response, 'Simple Planner')
        self.assertContains(response, 'https://simpleplanner.blottogbar.no')
        # Simple Flashcards
        self.assertContains(response, 'Simple Flashcards')
        self.assertContains(response, 'https://simplecards.blottogbar.no')
        # Simple Forum
        self.assertContains(response, 'Simple Forum')
        self.assertContains(response, 'https://simpleforum.blottogbar.no')

    def test_seo_meta_tags_and_structured_data(self):
        """Verify technical SEO: Canonical, robots, OpenGraph, and JSON-LD."""
        response = self.client.get(reverse('landing:index'))
        content = response.content.decode('utf-8')
        
        # Canonical URL
        self.assertIn('<link rel="canonical" href="https://www.blottogbar.no/">', content)
        
        # Robots meta
        self.assertIn('<meta name="robots"', content)
        
        # Open Graph
        self.assertIn('property="og:title"', content)
        self.assertIn('property="og:url" content="https://www.blottogbar.no/"', content)
        
        # JSON-LD Structured Data
        self.assertIn('type="application/ld+json"', content)
        self.assertIn('https://schema.org', content)
        self.assertIn('SoftwareApplication', content)
        self.assertIn('Simple Planner', content)
        self.assertIn('Simple Flashcards', content)
        self.assertIn('Simple Forum', content)

    def test_robots_txt(self):
        """Verify robots.txt endpoint returns valid text and references sitemap."""
        response = self.client.get(reverse('landing:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        content = response.content.decode('utf-8')
        self.assertIn('User-agent: *', content)
        self.assertIn('Sitemap: https://www.blottogbar.no/sitemap.xml', content)

    def test_sitemap_xml(self):
        """Verify sitemap.xml endpoint returns valid XML and includes all sub-apps."""
        response = self.client.get(reverse('landing:sitemap_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        content = response.content.decode('utf-8')
        self.assertIn('<loc>https://www.blottogbar.no/</loc>', content)
        self.assertIn('<loc>https://simpleplanner.blottogbar.no/</loc>', content)
        self.assertIn('<loc>https://simplecards.blottogbar.no/</loc>', content)
        self.assertIn('<loc>https://simpleforum.blottogbar.no/</loc>', content)

    def test_health_check(self):
        """Verify the health check endpoint returns JSON ok."""
        response = self.client.get(reverse('landing:health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok', 'app': 'blottogbar-landing'})

    def test_showcase_app_model(self):
        """Verify database model creation and string representation."""
        app = ShowcaseApp.objects.create(
            title='Custom Test App',
            slug='custom-test-app',
            tagline='A simple custom test tool',
            description='Detailed test description',
            url='https://custom.blottogbar.no',
            status='live',
            badge_label='Test Live'
        )
        self.assertEqual(str(app), 'Custom Test App (Live in Production)')
        
        response = self.client.get(reverse('landing:index'))
        self.assertContains(response, 'Custom Test App')
        self.assertContains(response, 'https://custom.blottogbar.no')
