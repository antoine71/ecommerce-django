from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from regex import D

from .models import Item, OrderItem, Order


def home(request):
    context = {"items": Item.objects.all()}
    return render(request, "home-page.html", context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.info(self.request, "Your cart is empty")
            return redirect('core:home')
        context = {
            'order': order,
            'order_items': order.items.all(),
            }
        return render(self.request, "order_summary.html", context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item_qs = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False,
    )
    if order_item_qs.exists():
        order = order_qs[0]
        order_item = order_item_qs[0]
        order_item.delete()
        messages.info(request, "The product was removed from your cart.")
        if not order.items.all().exists():
            order.delete()
    else:
        messages.info(request, "Error. the item was not in your cart.")
    return redirect("core:product", slug=slug)
