from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .filters import ProductFilter
from .forms import ProductForm



class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'flatpages/products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'flatpages/product.html'
    context_object_name = 'product'

class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('shop.add_product',)
    form_class = ProductForm
    model = Product
    template_name = 'flatpages/product_edit.html'

class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('shop.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'flatpages/product_edit.html'

class ProductDelite(PermissionRequiredMixin, DeleteView):
    permission_required = ('shop.delite_product',)
    model = Product
    template_name = 'flatpages/product_delite.html'
    success_url = reverse_lazy('products')
