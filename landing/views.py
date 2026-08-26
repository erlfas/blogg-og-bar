from django.shortcuts import render
from django.http import JsonResponse
from .models import ShowcaseApp


def index(request):
    """Main landing page for blottogbar.no."""
    db_apps = list(ShowcaseApp.objects.all())

    # Default featured showcase apps if database is not populated
    default_apps = [
        {
            'title': 'Simple Planner',
            'slug': 'simple-planner',
            'tagline': 'Rask og distrasjonsfri oppgave- og prosjektstyring.',
            'description': 'Et minimalistisk Kanban-brett bygget med fokus på hastighet, Markdown-støtte og ren oversikt. Ingen overflødige knapper eller tunge menyer.',
            'url': 'https://simpleplanner.blottogbar.no',
            'status': 'live',
            'badge_label': 'Live Nå',
            'ascii_icon': '┌─┬─┬─┐\n│█│▒│ │\n└─┴─┴─┘',
            'features': [
                'Lynrask Kanban-arbeidsflyt',
                'Dra-og-slipp oppgavestyring',
                'Innebygd Markdown & syntax highlighting',
                'Selvstendig og responsivt',
            ],
            'button_text': 'Åpne Simple Planner',
        },
        {
            'title': 'Focus Timer',
            'slug': 'focus-timer',
            'tagline': 'Ren tidsblokkering og arbeidsro.',
            'description': 'En enkel, visuell timer for dyp konsentrasjon. Null varsler, null støy — bare deg og oppgaven.',
            'url': '',
            'status': 'upcoming',
            'badge_label': 'Under utvikling',
            'ascii_icon': '╭──────╮\n│ 25:00│\n╰──────╯',
            'features': [
                'Pomodoro & flyt-intervaller',
                'Minimalistisk lydprofil',
                'Lokal statistikk',
            ],
            'button_text': 'Kommer snart',
        },
        {
            'title': 'Micro Notes',
            'slug': 'micro-notes',
            'tagline': 'Raske notater uten synk-forsinkelser.',
            'description': 'Fang tanker i farten med ren tekst. Eksporter til Markdown når du er klar.',
            'url': '',
            'status': 'upcoming',
            'badge_label': 'Konsept',
            'ascii_icon': '┌──────┐\n│ > _  │\n└──────┘',
            'features': [
                'Umiddelbar lasting',
                'Tastatursnarveier',
                'Markdown-først',
            ],
            'button_text': 'Kommer snart',
        },
    ]

    context = {
        'featured_app': default_apps[0],
        'apps': db_apps if db_apps else default_apps,
        'principles': [
            {
                'icon': '⚡',
                'title': 'Lynrask & Lettvekt',
                'desc': 'Ingen tunge rammeverk eller unødvendig JavaScript. Sidene og verktøyene laster på et blunk.',
            },
            {
                'icon': '🎯',
                'title': 'Ren funksjonalitet',
                'desc': 'Verktøy som løser én oppgave usedvanlig godt, uten reklame, bloat eller forvirrende menyer.',
            },
            {
                'icon': '🔒',
                'title': 'Personvern i høysetet',
                'desc': 'Dine data forblir dine. Ingen aggressive sporere eller unødvendige tredjeparts-skript.',
            },
        ],
    }
    return render(request, 'landing/index.html', context)


def health_check(request):
    """Simple health check endpoint for monitoring."""
    return JsonResponse({'status': 'ok', 'app': 'blottogbar-landing'})
