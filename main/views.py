from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def index_view(request):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0
    context = {
        'basket': basket,
        'banner':Banner.objects.all().order_by('-id')[:2],
        'product':Product.objects.all().order_by('id')[:8],
        'latest': Blog.objects.all().order_by('-id')[:4],
        'contact': Info.objects.last()

    }
    return render(request,'index.html', context)


def account_view(request):
    return render(request, 'account_settings.html')


def about_view(request):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0
    context = {
        'basket': basket,
        'about': About.objects.last(),
        'contact': Info.objects.last()

    }
    return render(request, 'about.html', context)


@login_required(login_url='/login/')
def add_basket(request, pk):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('login_url')
    product = Product.objects.get(pk=pk)
    Basket.objects.create(
        user=user,
        product=product,
    )
    return HttpResponse("Item added to basket successfully!")


def blog_view(request):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0
    context = {
        'blog':Blog.objects.all().order_by('-id')[:4],
        'category':Category.objects.all().order_by('-id')[:4],
        'tag':Tag.objects.all().order_by('-id')[:7],
        'basket': basket,
        'contact': Info.objects.last()
    }
    return render(request,'blog.html', context)


def blog_single_view(request, pk):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0
    blog = Blog.objects.get(pk=pk)
    context = {
        'basket': basket,
        'blog': blog,
        'recent_blog': Blog.objects.all().order_by('-id')[:5],
        'tag': Tag.objects.all().order_by('-id')[:3],
        'comment':Comment.objects.all().order_by('-id')[:3],
        'category': Category.objects.all().order_by('-id')[:4],
        'tag': Tag.objects.all().order_by('-id')[:7],
        'contact': Info.objects.last()
    }
    return render(request, 'blog-single.html', context)


@login_required(login_url='/login/')
def cart_view(request):
    basket = 0

    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = []

    products = []
    total = 0

    if basket != 0:
        product_counts = Basket.objects.filter(user_id=user.id).values('product').annotate(count=Count('id'))
        duplicate_products = [(product_count['product'], product_count['count']) for product_count in product_counts]

        for product_id, count in duplicate_products:
            product = Product.objects.get(id=product_id)
            products.append({'name': product, 'number': count, 'common': count * product.price})
            total += count * product.price
    context ={
        'products': products,
        'basket': basket,
        'total': total,
        'contact': Info.objects.last()
    }
    return render(request, 'cart.html', context)


def checkout_view(request):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
        products = Basket.objects.filter(user_id=user.id)
    else:
        basket = 0
        products = []
    total = 0
    for i in products:
        total += i.product.price
    context = {
        'basket': basket,
        "total": total,
        'contact': Info.objects.last()
    }
    return render(request, 'checkout.html', context)


def contact_view(request):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0

    contact = Info.objects.last()
    context = {
        'basket': basket,
        'contact': contact,

    }
    return render(request,'contact.html', context)


def create_contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        return redirect('contact_url')


def product_single(request, pk):
    product = Product.objects.get(pk=pk)
    related = Product.objects.filter(category=product.category).order_by('-id')[:4]
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0
    context = {
        'product': product,
        'related': related,
        'basket': basket,
        'contact': Info.objects.last()
    }
    return render(request, 'product-single.html', context)


def shop_view(request):
    categories = Category.objects.filter(is_active=True).order_by('-id')[:3]
    category = request.GET.get('category')
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user_id=user.id).count()
    else:
        basket = 0
    if category:
        products = Product.objects.filter(category__name=category)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj,
        'selected_category': category,
        'basket': basket,
        'contact': Info.objects.last()
    }
    return render(request, 'shop.html', context)


@login_required(login_url='/login/')
def add_basket_form(request, pk):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('login_url')
    number = request.POST.get('number')
    product = Product.objects.get(pk=pk)
    if number.isdigit():
        for _ in range(int(number)):
            Basket.objects.create(
                user=user,
                product=product,
            )
    return redirect('product_single_url', pk=pk)


@login_required(login_url='/login/')
def remove_cart_product(request, pk, id):
    product = Product.objects.get(pk=id)
    basket = Basket.objects.filter(user_id=pk, product_id=product)
    basket.delete()
    return redirect('cart_url')


def create_comment(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = 'AnonimUser'
    if request.method == "POST":
        text = request.POST['text']
        Comment.objects.create(
        user= user,
        blog = blog,
        text = text,
        )
    return redirect('blog_single_url', blog.id)


@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        new_username = request.POST.get('username')

        if User.objects.filter(username=new_username).exists() and user.username != new_username:
            context = {'message': 'Ushbu foydalanuvchi nomi band. Iltimos, boshqa nom kiriting.', "error": True, 'user':user}
            return render(request, 'account_settings.html', context)

        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_phone_number = request.POST.get('phone_number')
        new_mobile_number = request.POST.get('mobile_number')
        new_email = request.POST.get('email')
        new_address = request.POST.get('address')

        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.phone_number = new_phone_number
        user.mobile_number = new_mobile_number
        user.email = new_email
        user.address = new_address
        user.save()

        context = {'message': 'Foydalanuvchi ma\'lumotlari muvaffaqiyatli yangilandi.', 'user': user}
        return render(request, 'account_settings.html', context)

    return render(request, 'edit_profile.html', {'user': user})


@login_required(login_url='/login/')
def edit_password_user(request):
    user = request.user
    if request.method == 'POST':
        current_pass = request.POST.get('current_pass')
        new_pass = request.POST.get('new_pass')
        again_new_pass = request.POST.get('again_new_pass')


        auth_user = authenticate(username=user.username, password=current_pass)
        if auth_user is not None:
            if new_pass == again_new_pass:
                # Yangi parolni sozlash
                user.set_password(new_pass)
                user.save()

                # Yangi parol bilan foydalanuvchini avtorizatsiya qilish
                login(request, user)

                context = {'message': 'Foydalanuvchi paroli muvaffaqiyatli o\'zgartirildi.', 'user': user}
                return render(request, 'account_settings.html', context)
            else:
                context = {'message': 'Parollar mos emas.', 'user': user}
                return render(request, 'account_settings.html', context)
        else:
            context = {'message': "Eski parol not'g'ri kiritildi", 'user': user}
            return render(request, 'account_settings.html', context)
    context = {'user':user}
    return render(request, 'account_settings.html', context)



@login_required(login_url='/login/')
def create_order(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        street = request.POST.get('street')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        products = ""
        total = 0
        user = request.user
        product_counts = Basket.objects.filter(user_id=user.id).values('product').annotate(count=Count('id'))
        duplicate_products = [(product_count['product'], product_count['count']) for product_count in product_counts]

        for product_id, count in duplicate_products:
            product = Product.objects.get(id=product_id)
            products += f"Maxsulot nomi: {product.title}, Maxsulot soni {count}, Maxsulot narxi: {product.price}, Maxsulot umumiy summasi: {count*product.price}"
            total += count * product.price
        Order.objects.create(
            firstname=firstname,
            lastname=lastname,
            street=street,
            city=city,
            phone_number=phone_number,
            products=products,
            total=total
        )
        return redirect('index_url')


@login_required(login_url='/login/')
def update_cart(request, pk):
    user = request.user
    if request.method == 'POST':
        number = int(request.POST.get('number'))
        basket = Basket.objects.filter(user=user, product_id=pk)
        product = Product.objects.get(pk=pk)
        if number > basket.count():
            numbers = number-basket.count()
            for i in range(numbers):
                Basket.objects.create(
                    user=user,
                    product=product
                )
        elif number < basket.count():
            numbers = basket.count() - number
            for i in range(numbers):
                basket[0].delete()
        elif number == 0:
            basket.delete()
    return redirect('cart_url')





def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr = authenticate(
            username=username,
            password=password
        )
        if usr is not None:
            login(request, usr)
            return redirect('index_url')
        else:
            context = {
                'error': True
            }
            return render(request, 'login.html', context)

    return render(request, 'login.html')


def sing_up_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            context = {
                'band': True,
            }
            return render(request, 'sign-up.html', context)
        else:
            User.objects.create_user(
                username=username,
                password=password,
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number,
                email = email
            )
            return redirect('index_url')
    return render(request, 'sign-up.html')


def user_logout(request):
    logout(request)
    return redirect('index_url')
