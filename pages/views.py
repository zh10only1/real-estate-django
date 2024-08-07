from gettext import gettext
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from .models import Privacy, Topbar, Article, Translation
from listings.choices import price_choices, bedroom_choices, state_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator  ## For Pagination
from translate import Translator

# Create your views here.

def index(request):

    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    tb = Topbar.objects.get()

    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'tb': tb
    }

    return render(request, 'pages/index.html', context)


def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')
    tb = Topbar.objects.get()

    # Get MVP (Seller of the month)
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors,
        'tb': tb
    }

    return render(request, 'pages/about.html', context)


def privacy(request):
    p = Privacy.objects.order_by('-created')
    tb = Topbar.objects.get()
    context = {
        'p': p,
        'tb': tb,
    }
    return render(request, 'pages/privacy.html', context)


def article(request):

    article = Article.objects.order_by('-created').filter(is_published=True)
    tb = Topbar.objects.get()
    ### Pagination Start ###
    paginator = Paginator(article, 6)   ## how much item i want to show in each page
    page = request.GET.get('page')
    paged_interface = paginator.get_page(page)
    ### Pagination End ###
    context = {
        'interface': paged_interface,
        'article': article,
        'tb': tb,
        # 'title': title,
    }
    return render(request, 'pages/article.html', context)


def articleDetail(request, inter_id):

    article_details = get_object_or_404(Article, pk=inter_id)   ## if page doesn't exist, it will show page not found(error message)
    tb = Topbar.objects.get()
    context = {
        'article_details': article_details,
        'tb': tb,
    }

    return render(request, 'pages/article-detail.html', context)


def translate_all(request):
    translation = Translation.objects.all()

    err_msg = "MYMEMORY WARNING"

    language_short_form = {'German': 'de', 'French': 'fr', 'Greek': 'el', 'Croatian': 'hr', 'Polish': 'pl',
                           'Czech': 'cs', 'Russian': 'ru', 'Swedish': 'sv', 'Norway': 'no', 'Slovak': 'sk',
                           'Dutch': 'nl', 'English': 'en'}  # 'English': 'en',
    for key, value in language_short_form.items():
        translator = Translator(from_lang='de', to_lang=value)
        for t in translation:
            if key == 'German':
                if t.german_content != '' and err_msg not in t.german_content: continue
                t.german_content = translator.translate(t.german_content)
            elif key == 'French':
                if t.french_content != '' and err_msg not in t.french_content: continue
                t.french_content = translator.translate(t.german_content)
            elif key == 'Greek':
                if t.greek_content != '' and err_msg not in t.greek_content: continue
                t.greek_content = translator.translate(t.german_content)
            elif key == 'Croatian':
                if t.croatian_content != '' and err_msg not in t.croatian_content: continue
                t.croatian_content = translator.translate(t.german_content)
            elif key == 'Polish':
                if t.polish_content != '' and err_msg not in t.polish_content: continue
                t.polish_content = translator.translate(t.german_content)
            elif key == 'Czech':
                if t.czech_content != '' and err_msg not in t.czech_content: continue
                t.czech_content = translator.translate(t.german_content)
            elif key == 'Russian':
                if t.russian_content != '' and err_msg not in t.russian_content: continue
                t.russian_content = translator.translate(t.german_content)
            elif key == 'Swedish':
                if t.swedish_content != '' and err_msg not in t.swedish_content: continue
                t.swedish_content = translator.translate(t.german_content)
            elif key == 'Norway':
                if t.norway_content != '' and err_msg not in t.norway_content: continue
                t.norway_content = translator.translate(t.german_content)
            elif key == 'Slovak':
                if t.slovak_content != '' and err_msg not in t.slovak_content: continue
                t.slovak_content = translator.translate(t.german_content)
            elif key == 'Dutch':
                if t.dutch_content != '' and err_msg not in t.dutch_content: continue
                t.dutch_content = translator.translate(t.german_content)
            elif key == 'English':
                if t.english_content != '' and err_msg not in t.english_content: continue
                t.english_content = translator.translate(t.german_content)
            t.save()
            print(f'{key} Translation Completed for {t.german_content}')
    return HttpResponse('Translation Completed')