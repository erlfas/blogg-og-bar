from django.shortcuts import render
from django.http import JsonResponse
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
            'features': [
                'Tavlevisning (Kanban)',
                'Dra-og-slipp av oppgaver',
                'Støtte for Markdown',
                'Rent grensesnitt',
            ],
            'button_text': 'Gå til Simple Planner',
        },
    ]

    context = {
        'apps': db_apps if db_apps else default_apps,
        'principles': [
            {
                'title': 'Avgrenset kjernefunksjonalitet',
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
