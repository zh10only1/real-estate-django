from django.utils.translation import activate
from pages.models import Translation

def set_language(request):
    lang = request.session.get('site_language', 'en')
    activate(lang)
    return {'language': lang}


def get_my_translations(request):
    current_path = request.path
    page = 'home'
    if current_path == '/': page = 'home'
    elif current_path == '/about/': page = 'about'
    elif '/listing/' in current_path: page = 'listings'
    elif '/profile/' in current_path: page = 'profile'
    elif '/blog/' in current_path: page = 'blog'
    elif '/contact/' in current_path: page = 'contact'
    elif '/login' in current_path: page = 'login'
    elif '/register' in current_path: page = 'signup'
    elif '/property-details/' in current_path: page = 'property details'
    elif '/profile' in current_path: page = 'profile'
    elif '/add-property/' in current_path: page = 'add-property'
    elif '/privacy/' in current_path: page = 'privacy'
    elif '/blog/' in current_path: page = 'blog'
    elif '/forget-password/' in current_path: page = 'forget-password'
    elif '/verify-otp/' in current_path: page = 'reset-password'
    elif '/blog/single/' in current_path: page = 'blog details'

    user_language = request.session.get('site_language', 'en')

    context = {}
    translations = Translation.objects.filter(page=page) | Translation.objects.filter(page='navbar') | Translation.objects.filter(page='footer')
    for t in translations:
        if user_language == 'en': context[t.name] = t.english_content
        elif user_language == 'ge': context[t.name] = t.german_content
        elif user_language == 'fr': context[t.name] = t.french_content
        elif user_language == 'gr': context[t.name] = t.greek_content
        elif user_language == 'hr': context[t.name] = t.croatian_content
        elif user_language == 'pl': context[t.name] = t.polish_content
        elif user_language == 'cz': context[t.name] = t.czech_content
        elif user_language == 'ru': context[t.name] = t.russian_content
        elif user_language == 'sw': context[t.name] = t.swedish_content
        elif user_language == 'no': context[t.name] = t.norway_content
        elif user_language == 'sk': context[t.name] = t.slovak_content
        elif user_language == 'nl': context[t.name] = t.dutch_content

    return context