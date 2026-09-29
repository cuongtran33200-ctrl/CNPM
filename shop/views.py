import base64
from io import BytesIO

import qrcode
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import AddToCartForm, CheckoutForm, ProfileForm, RegisterForm, ReviewForm, SupportRequestForm
from .models import Category, Order, OrderItem, Product, Review, SupportRequest


def build_qr_data_uri(amount, order_id=None):
    order_label = f"DON HANG #{order_id}" if order_id else "DON HANG MOI"
    qr_content = f"SBCB SHOP | {order_label} | SO TIEN {amount:.0f} VND"
    qr_image = qrcode.make(qr_content)
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded_image}"


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(slug__icontains=query)
        ).distinct()

    context = {
        "category": category,
        "categories": categories,
        "products": products,
        "query": query or "",
    }
    return render(request, "shop/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    form = AddToCartForm()
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    review_form = None
    user_can_review = False
    if request.user.is_authenticated:
        already_reviewed = Review.objects.filter(product=product, user=request.user).exists()
        has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()
        user_can_review = has_purchased and not already_reviewed
        if user_can_review:
            review_form = ReviewForm()

    context = {
        "product": product,
        "form": form,
        "related_products": related_products,
        "reviews": product.reviews.all().select_related("user"),
        "review_form": review_form,
        "user_can_review": user_can_review,
    }
    return render(request, "shop/product_detail.html", context)


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()
    if not has_purchased:
        messages.error(request, "Bạn cần mua sản phẩm này trước khi đánh giá.")
        return redirect(product.get_absolute_url())
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.warning(request, "Bạn đã đánh giá sản phẩm này rồi.")
        return redirect(product.get_absolute_url())

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Cảm ơn bạn đã đánh giá sản phẩm!", extra_tags="confetti")
    return redirect(product.get_absolute_url())


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"])
        messages.success(request, f"Đã thêm \"{product.name}\" vào giỏ hàng.")
    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Đã xoá \"{product.name}\" khỏi giỏ hàng.")
    return redirect("shop:cart_detail")


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    if quantity < 1:
        cart.remove(product)
    else:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    return redirect("shop:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart_detail.html", {"cart": cart})


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Giỏ hàng của bạn đang trống.")
        return redirect("shop:product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )
            cart.clear()
            messages.success(
                request,
                "Đặt hàng thành công! Cảm ơn bạn đã mua sắm tại SBCB.",
                extra_tags="confetti",
            )
            return redirect("shop:order_detail", order_id=order.id)
    else:
        initial = {}
        if request.user.first_name:
            initial["full_name"] = request.user.first_name
        form = CheckoutForm(initial=initial)

    return render(request, "shop/checkout.html", {
        "cart": cart,
        "form": form,
        "qr_code": build_qr_data_uri(cart.get_total_price()),
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "shop/order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_detail.html", {
        "order": order,
        "qr_code": build_qr_data_uri(order.total_price, order.id),
    })


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Chào mừng {user.username} đến với SBCB!")
            return redirect("shop:product_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            form.save()
            messages.success(request, "Đã cập nhật hồ sơ cá nhân.")
            return redirect("shop:profile")
    else:
        form = ProfileForm(
            instance=profile,
            initial={"first_name": request.user.first_name, "email": request.user.email},
        )
    return render(request, "shop/profile.html", {"form": form})


@login_required
def support_create(request):
    if request.method == "POST":
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            support_req = form.save(commit=False)
            support_req.user = request.user
            support_req.save()
            messages.success(request, "Đã gửi yêu cầu hỗ trợ. Nhân viên sẽ phản hồi sớm nhất.")
            return redirect("shop:support_list")
    else:
        form = SupportRequestForm()
    my_requests = SupportRequest.objects.filter(user=request.user)
    return render(request, "shop/support.html", {"form": form, "my_requests": my_requests})
