from django.core.checks import messages
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.shortcuts import render
from django.db.models import Q
from .forms import SearchForm
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
#category
from product.models import Category, Product, Images, Comment, Variants
from myapp import settings
from user.models import UserProfile


# Create your views here.
from product.models import CategoryLang


def index(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    # categories = Category.objects.filter(Q(mptt_level=0) | Q(mptt_level=1))
    product_feature = Product.objects.all().order_by('-id')[:6]
    product_recommended = Product.objects.all().order_by('?')[:6]
    product_slider = Product.objects.all().order_by('-id')[:4]  # first 4 products

    setting = Setting.objects.get(pk=1)
    product_lasted = Product.objects.all().order_by('-id')[:4]

    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
        product_feature = Product.objects.raw(
            'SELECT p.id,p.price, l.title, l.description,l.slug  '
            'FROM product_product as p '
            'LEFT JOIN product_productlang as l '
            'ON p.id = l.product_id '
            'WHERE  l.lang=%s ORDER BY p.id DESC LIMIT 6', [currentlang])

    context = {
        'title': 'TSDI Home-Ecommerce',
        #'categories': categories,
        'setting': setting,
        'product_slider': product_slider,
        'product_feature': product_feature,
        'product_lasted': product_lasted,
        'product_recommended': product_recommended,

    }
    return render(request, 'index.html', context)


def about(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Setting.objects.get(pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    context = {
        'title': 'About',
        'setting': setting,
    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message has been sent. Thank you your message")
            return HttpResponseRedirect('/contact')

    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Setting.objects.get(pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    form = ContactForm
    context = {
        'title': 'Contact',
        'form': form,
        'setting': setting,
    }
    return render(request, 'contact.html', context)


def category(request, id, slug):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    catdata = Category.objects.get(pk=id)
    product_slider = Product.objects.all().order_by('-id')[:4]
    setting = Setting.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)  # default language
    if defaultlang != currentlang:
        try:
            products = Product.objects.raw(
                'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                'FROM product_product as p '
                'LEFT JOIN product_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.category_id=%s and l.lang=%s', [id, currentlang])
        except:
            pass
        catdata = CategoryLang.objects.get(category_id=id, lang=currentlang)

    context = {'products': products,
               'setting': setting,
               'product_slider': product_slider,
               'catdata': catdata
               }
    return render(request, 'categorys.html', context)


def product_detail(request, id, slug):
    query = request.GET.get('q')

    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]  # en-EN
    currentlang = request.LANGUAGE_CODE[0:2]
    # category = categoryTree(0, '', currentlang)
    categories = Category.objects.filter(Q(mptt_level=0) | Q(mptt_level=1))

    product = Product.objects.get(pk=id)

    if defaultlang != currentlang:
        try:
            prolang = Product.objects.raw(
                'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                'FROM product_product as p '
                'INNER JOIN product_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.id=%s and l.lang=%s', [id, currentlang])
            product = prolang[0]
        except:
            pass
    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end

    setting = Setting.objects.get(pk=1)

    images = Images.objects.filter(product_id=id)
    product_recommended = Product.objects.all().order_by('?')[:6]
    comments = Comment.objects.filter(status=True, product_id=id)

    context = {'title': 'Product Detail', 'setting': setting, 'product': product, 'images': images, 'comments': comments, 'categories': categories, 'product_recommended':product_recommended}

    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query
                        })
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def search(request):
    product_slider = Product.objects.all().order_by('-id')[:3]
    categories = Category.objects.filter(Q(mptt_level=0) | Q(mptt_level=1))
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)# select * from product where title like '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()

            context = {
                'products': products,
                'query': query,
                'category': category,
                'product_slider': product_slider,
                'categories': categories,
            }
            return render(request, 'search_product.html', context)

    return HttpResponseRedirect('/')


def faq(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    categories = Category.objects.filter(Q(mptt_level=0) | Q(mptt_level=1))
    if defaultlang == currentlang:
        faq = FAQ.objects.filter(status="True", lang=defaultlang).order_by("ordernumber")
    else:
        faq = FAQ.objects.filter(status="True", lang=currentlang).order_by("ordernumber")

    context = {
        'categories': categories,
        'faq': faq,
    }

    return render(request, 'faq.html', context)


def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
        #return HttpResponse(lang)
        return HttpResponseRedirect("/"+lang)


def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)


@login_required(login_url='/login') # Check login
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    language=Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    #Save to User profile database
    data = UserProfile.objects.get(user_id=curren_user.id )
    data.language_id = language.id
    data.currency_id = request.session['currency']
    data.save()  # save data
    return HttpResponseRedirect(lasturl)