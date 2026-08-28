from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ShowcaseApp


def index(request):
    """Hovedside for blottogbar.no."""
    db_apps = list(ShowcaseApp.objects.all())

    default_apps = [
        {
            'title': 'Simple Planner',
            'slug': 'simple-planner',
            'tagline': 'Enkel oppgavestyring basert på Kanban.',
            'description': 'Et minimalistisk verktøy for strukturering av oppgaver med tavlevisning og støtte for Markdown. Bygget for å gi oversikt uten overflødige valg.',
            'url': 'https://simpleplanner.blottogbar.no',
            'status': 'live',
            'badge_label': 'Tilgjengelig',
            'ascii_icon': '┌─┬─┬─┐\n│█│▒│ │\n└─┴─┴─┘',
            'category': 'ProjectManagementApplication',
            'features': [
                'Tavlevisning (Kanban)',
                'Dra-og-slipp av oppgaver',
                'Støtte for Markdown',
                'Rent grensesnitt',
            ],
            'button_text': 'Gå til Simple Planner',
        },
        {
            'title': 'Simple Flashcards',
            'slug': 'simple-flashcards',
            'tagline': 'Repetisjonskort med SM-2-algoritmen.',
            'description': 'Effektiv innlæring basert på tidsintervallert repetisjon (Spaced Repetition). Støtter Markdown og matematiske formler med LaTeX.',
            'url': 'https://simplecards.blottogbar.no',
            'status': 'live',
            'badge_label': 'Tilgjengelig',
            'ascii_icon': '┌─────┐\n│[ ? ]│\n└─────┘',
            'category': 'EducationalApplication',
            'features': [
                'SM-2 repetisjonsalgoritme',
                'Støtte for Markdown og LaTeX',
                'Tastatursnarveier',
                'Distrasjonsfritt grensesnitt',
            ],
            'button_text': 'Gå til Simple Flashcards',
        },
        {
            'title': 'Simple Forum',
            'slug': 'simple-forum',
            'tagline': 'Tekstbasert og lineært diskusjonsforum.',
            'description': 'Et uforstyrret diskusjonsforum med fokus på saklig tekst. Uten emojier, bilder, likes eller algoritmiske tidslinjer.',
            'url': 'https://simpleforum.blottogbar.no',
            'status': 'live',
            'badge_label': 'Tilgjengelig',
            'ascii_icon': '┌─────┐\n│ > _ │\n└─────┘',
            'category': 'DiscussionForumApplication',
            'features': [
                'Lineære diskusjonstråder',
                'Fulltekstsøk',
                'Ingen emojier eller bildeopplasting',
                'Rent tekstfokus',
            ],
            'button_text': 'Gå til Simple Forum',
        },
    ]

    context = {
        'apps': db_apps if db_apps else default_apps,
        'principles': [
            {
                'title': 'Avgrenset funksjonalitet',
                'desc': 'Hver applikasjon løser en avgrenset oppgave og leverer kun nødvendig funksjonalitet. Når verktøyet fungerer etter hensikten, anses det som ferdig. Vi unngår kontinuerlig tilførsel av nye funksjoner som skaper unødvendig kompleksitet.',
            },
            {
                'title': 'Sikker og ressurseffektiv drift',
                'desc': 'Videre forbedringer er begrenset til å opprettholde en stabil, sikker og kostnadseffektiv arkitektur med lavest mulig ressursbruk.',
            },
            {
                'title': 'Gratis og uten reklame',
                'desc': 'Tjenestene er gratis å benytte. Løsningene inneholder ingen reklame, kommersielle bindinger eller sporing.',
            },
        ],
    }
    return render(request, 'landing/index.html', context)


def health_check(request):
    """Enkelt endepunkt for helsesjekk."""
    return JsonResponse({'status': 'ok', 'app': 'blottogbar-landing'})


def robots_txt(request):
    """SEO robots.txt fil."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: https://www.blottogbar.no/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """SEO sitemap.xml fil."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.blottogbar.no/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://simpleplanner.blottogbar.no/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://simplecards.blottogbar.no/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://simpleforum.blottogbar.no/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""
    return HttpResponse(xml_content.strip(), content_type="application/xml")
