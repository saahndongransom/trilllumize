from django.shortcuts import render, get_object_or_404
from myapp.models import BlogPost
from myapp.models import Category, Tag, Comment
#from .models import BlogPost, Category, Tag
from .forms import CommentForm
from django.shortcuts import  redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from .models import SubscribedUsers  # Import your custom model if used.
from .forms import NewsletterForm
from .models import Resource
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Cart, CartItem
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.urls import reverse  
from django.shortcuts import render, redirect
from .models import Resource, CartItem
from .forms import OrderForm
from .utils import calculate_cart_total
from django.db.models import Q

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO








def about(request):
    return render(request, 'about.html')





def contact(request):
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send the form data via email (replace 'your_email@example.com' with your email address)
            send_mail(
                subject=f"Contact Form Submission - {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=email,
                recipient_list=['saahndongransom@gmail.com'],
            )

            # Set success to True to show the success message in the template
            success = True

            # Reset the form to show an empty form after successful submission
            form = ContactForm()

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'success': success})






def blog_list(request):
    blog_posts = BlogPost.objects.order_by('pub_date')  # Change '-' to remove descending order
    recent_posts = BlogPost.objects.order_by('-pub_date')[:3]
    return render(request, 'blog_list.html', {'blog_posts': blog_posts, 'recent_posts': recent_posts})

def index(request):
    blog_posts = BlogPost.objects.order_by('pub_date')  # Change '-' to remove descending order
    recent_posts = BlogPost.objects.order_by('-pub_date')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'index.html', {'blog_posts': blog_posts, 'recent_posts': recent_posts, 'categories': categories, 'tags': tags})


def blog(request, tag_slug=None):
    blog_posts = BlogPost.objects.order_by('-pub_date')
    recent_posts = BlogPost.objects.order_by('-pub_date')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    selected_tag = None

    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        blog_posts = blog_posts.filter(tags=selected_tag)

    # Handling search query
    query = request.GET.get('q')
    if query:
        blog_posts = blog_posts.filter(
            Q(title__icontains=query) |  # Search in the title for a case-insensitive match
            Q(content__icontains=query)  # Search in the content for a case-insensitive match
        )

    # Pagination
    page = request.GET.get('page', 1)  # Get the current page number from the URL parameter 'page'
    per_page = 6  # Number of blog posts to display per page
    paginator = Paginator(blog_posts, per_page)

    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {
        'blog_posts': blog_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
        'selected_tag': selected_tag,
    })

def blog_with_tag(request, tag_slug):
    blog_posts = BlogPost.objects.filter(tags__slug=tag_slug)
    recent_posts = BlogPost.objects.order_by('-pub_date')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    page = request.GET.get('page', 1)  # Get the current page number from the URL parameter 'page'
    per_page = 1  # Number of blog posts to display per page
    paginator = Paginator(blog_posts, per_page)

    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)
    return render(request, 'blog.html', {
        'blog_posts': blog_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
        'selected_tag': tag_slug,  # Pass the selected tag slug to the template
    })
    return render(request, 'blog_with_tag.html', {'blog_posts': blog_posts, 'tag': tag})


def post_details(request, post_slug):
    blog_post = get_object_or_404(BlogPost, slug=post_slug)
    recent_posts = BlogPost.objects.order_by('-pub_date')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog_post
            comment.save()
            # Redirect to the same post details page after successful comment submission
            return redirect('post_details', post_slug=post_slug)
    else:
        form = CommentForm()

    return render(request, 'post_details.html', {
        'blog_post': blog_post,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
        'form': form,
    })

def blog_with_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    blog_posts = BlogPost.objects.filter(categories=category)
    recent_posts = BlogPost.objects.order_by('-pub_date')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
 # Pagination
    page = request.GET.get('page', 1)  # Get the current page number from the URL parameter 'page'
    per_page = 1  # Number of blog posts to display per page
    paginator = Paginator(blog_posts, per_page)

    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {
        'blog_posts': blog_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
          # Pass the selected tag slug to the template
    })

    # You can also pass the 'category' object to the template to display the category name if needed.
    return render(request, 'blog_with_category.html', {'blog_posts': blog_posts, 'category': category})


from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import NewsletterForm

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # Code to send email
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            email_from = request.user.email if request.user.is_authenticated else form.cleaned_data.get('email')

            try:
                mail = EmailMessage(subject, email_message, email_from, bcc=receivers)
                mail.content_subtype = "html"  # Set the email content type to "text/html"
                mail.send()
                messages.success(request, "Email sent successfully")
            except Exception as e:
                messages.error(request, f"There was an error sending email: {str(e)}")
        else:
            messages.error(request, "One or more required fields are missing")

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request, 'newsletter.html', {'form': form})







def subscribe(request):
    print(request.method)
    print(request.method, "method")
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, "You must type legit name and email to subscribe to a Newsletter")
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            print(f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            print(f"{email} email address is already subscriber.")
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers(email=email)
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))




def resource_list(request):
    resources = Resource.objects.all()
    cart = request.session.get('cart', {})
    cart_items = []

    for resource_id, item in cart.items():
        cart_items.append(item)
        
    return render(request, 'resource_list.html', {'resources': resources, 'cart_items': cart_items})


@login_required
def purchase_resource_view(request, resource_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('register')  # Redirect to the registration page

    # Logic to handle the resource purchase and access granting
    # ...
    return render(request, 'purchase_resource.html', {'resource_id': resource_id})


from django.contrib.auth.forms import UserCreationForm

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def add_to_cart(request, resource_id):
    cart = request.session.get('cart', {})
    resource = get_object_or_404(Resource, pk=resource_id)

    if resource_id in cart:
        cart[resource_id]['quantity'] += 1
    else:
        cart[resource_id] = {
            'id': resource.id,
            'title': resource.title,
            'price': float(resource.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    print(request.session['cart'])
    messages.success(request, f"{resource.title} has been added to your cart.")

    if request.user.is_authenticated:
        return redirect('resource_list')
    else:
        return redirect('login')



def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = list(cart.values())
    
    # Calculate the total price of each cart item based on the quantity
    for item in cart_items:
        item['total_price'] = item['price'] * item['quantity']
    
    cart_total = sum(item['total_price'] for item in cart_items)
    cart_count = sum(item['quantity'] for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total, 'cart_count': cart_count})

def remove_from_cart(request, cart_item_id):
    cart = request.session.get('cart', {})
    cart_item_id = str(cart_item_id)

    if cart_item_id in cart:
        del cart[cart_item_id]
        request.session['cart'] = cart
        messages.success(request, "Item removed from the cart.")
    else:
        messages.error(request, "Item not found in the cart.")

    return redirect('view_cart')



def update_cart_quantity(request, cart_item_id):
    cart = request.session.get('cart', {})
    cart_item_id = str(cart_item_id)

    if cart_item_id in cart:
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart[cart_item_id]['quantity'] = new_quantity
            # Recalculate the item price after updating the quantity
            cart[cart_item_id]['price'] = float(cart[cart_item_id]['price']) * new_quantity
            request.session['cart'] = cart
            messages.success(request, "Quantity updated.")
        else:
            messages.error(request, "Invalid quantity.")
    else:
        messages.error(request, "Item not found in the cart.")

    return redirect('view_cart')








@login_required
def logout(request):
    auth_logout(request)
    return redirect('resource_list')


def clear_messages(request):
    # Clear messages from the session
    storage = messages.get_messages(request)
    storage.used = True
    return JsonResponse({'status': 'ok'})
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render(request, 'resource_detail.html', {'resource': resource})
def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': cart_count})
















def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for resource_id, item in cart.items():
        cart_items.append(item)

    if not cart_items:
        return redirect('resource_list')  # Redirect to resource page if cart is empty

    cart_total = calculate_cart_total(cart_items)

    # Process the form submission
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the order and process the payment here
            # ... (your payment processing logic goes here)
            # After successful payment processing, you can clear the cart session
            request.session['cart'] = {}

            # Use reverse to get the URL for the order_success view with cart_total as a query parameter
            return redirect(reverse('order_success') + f'?cart_total={cart_total}')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total, 'form': form})

def payment_process(request):
    if request.method == 'POST':
        # Implement your payment processing logic here
        # For example, you can charge the user's credit card, process the payment, etc.

        # After successful payment, you might want to clear the cart
        request.session['cart'] = {}
        messages.success(request, "Payment successful. Your order has been processed.")

        return redirect('resource_list')  # Redirect the user to the resource list page after payment

    # If the request method is not POST (e.g., user accesses the page directly via URL),
    # you can redirect them to the cart page or any other appropriate page.
    # For this example, we'll redirect them to the cart page.
    messages.error(request, "Invalid request. Please proceed to the checkout page.")
    return redirect('cart')


def order_success(request):
    cart_total = request.GET.get('cart_total', 0.0)  # Get the cart_total from the query parameters
    # ... (other logic)
    return render(request, 'order_success.html', {'cart_total': cart_total})



def generate_receipt(request):
    # Get the cart_total from the query parameters
    cart_total = float(request.GET.get('cart_total', 0.0))

    # Create a PDF object
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Customize your receipt design here
    # For example, you can use p.drawString() to add text to the PDF

    # Draw the cart_total on the PDF
    p.drawString(100, 100, f'Total: ${cart_total:.2f}')

    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and return it as a downloadable PDF
    pdf = buffer.getvalue()
    buffer.close()

    # Set the content type and content disposition for the HTTP response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    return response



