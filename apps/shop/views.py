from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models.query import QuerySet
from django.http import Http404
from django.core.paginator import Paginator

from apps.shop.forms import ReviewForm
from apps.shop.utils import sort_products, sort_filter_value

from apps.shop.models import  Category, Product

class HomeView(View):
    def get(self, request):
        products = Product.objects.all()[:6]
        categories = Category.objects.all()
        context = {
            "products": products,
            "categories": categories,
        }
        return render(request, 'shop/home.html', context)
    
class ProductListView(ListView): 
    model = Product
    paginate_by = 15
    template_name = "shop/product_list.html"
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[Product]:
        products = Product.objects.prefetch_related("reviews")
        products = sort_products(self.request, products)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_filter_value(self.request, context)
        return context

class ProductDetailView(View): 
    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.select_related("category").prefetch_related("reviews", "reviews__customer").get(slug=kwargs["slug"])
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        form = ReviewForm()
        context = {
            "product": product,
            "form": form
        }
        return render(request, 'shop/product_detail.html', context)
    
class CategoriesView(ListView):
    model = Category
    template_name = "shop/categories.html"
    context_object_name = "categories"
    
class CategoryProductsView(View):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs["slug"])
        products = Product.objects.filter(category=category).prefetch_related("reviews")
        products = sort_products(self.request, products)

        # Pagination config
        paginated = Paginator(products, 15)
        page_number = request.GET.get('page')
        page = paginated.get_page(page_number)
        is_paginated = True if page.paginator.num_pages > 1 else False

        context = {"category": category, "page_obj": page, "is_paginated": is_paginated}
        sort_filter_value(self.request, context)
        return render(request, "shop/category_products.html", context)
    
