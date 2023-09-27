from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from qcqualitycontrol.core.views import WebsiteView
from .forms import ContactForm
from .forms import NotesForm
from .models import Category
from .models import Product
from .models import File


class ContentView(WebsiteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = Category.objects.filter(parent=None)
        return context


class IndexView(ContentView):
    template_name = 'qc_index.html'


class ContactView(FormMixin, ContentView):
    template_name = 'qc_contact.html'
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            subject = 'Inquiry'
            message = 'Name: {name}<br>' \
                      'Company: {company}<br>' \
                      'E-Mail: {email}<br>' \
                      'Phone: {phone}<br>' \
                      'Message: {message}<br>'.format(**form.cleaned_data)
            # don't allow spam
            if ('http' in message) or ('https' in message) or ('noreply' in message) or ('Company: google' in message):
                return JsonResponse({'status': 'fail'})
            # end don't allow spam
            from_mail = 'projekte@tortuga-webdesign.de'
            recipient_list = ['projekte@tortuga-webdesign.de', 'info@qc-quality-control.de']
            send_mail(subject, message, from_mail, recipient_list, html_message=message)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'fail'})


class CompanyProfileView(ContentView):
    template_name = 'qc_companyprofile.html'


class CertificatesView(ContentView):
    template_name = 'qc_certificates.html'


class ProductsSearchView(ContentView):
    template_name = 'qc_products_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search:
            context['search'] = search
            context['category_items'] = {}
            products = Product.objects\
                .filter(Q(name__icontains=search) | Q(sub__icontains=search) | Q(categories__name__icontains=search))\
                .order_by('name').distinct()
            files = File.objects \
                .filter(Q(name__icontains=search) | Q(sub__icontains=search) | Q(categories__name__icontains=search)) \
                .order_by('name').distinct()
            context['category_items']['Found'] = {}
            context['category_items']['Found']['products'] = products
            context['category_items']['Found']['files'] = files
        return context


class ProductsView(ContentView):
    template_name = 'qc_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=kwargs['slug'])
        context['category'] = category
        bottom_categories = category.get_bottom()
        context['category_items'] = {}
        for c in bottom_categories:
            context['category_items'][c.name] = {}
            context['category_items'][c.name]['products'] = c.get_products()
            context['category_items'][c.name]['files'] = c.get_files()
        context['children'] = category.children.all()
        return context


class FileView(ContentView):
    template_name = 'qc_file.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file = get_object_or_404(File, slug=kwargs['slug'])
        context['file'] = file
        return context


class ProductView(FormMixin, ContentView):
    template_name = 'qc_product.html'
    form_class = NotesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=kwargs['slug'])
        context['product'] = product
        return context

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        form = self.get_form()
        if form.is_valid():
            notes = '{notes}'.format(**form.cleaned_data)
            product.set_notes_mark(notes)
        else:
            product.set_notes_mark('')
        return HttpResponseRedirect(reverse_lazy('content:product', args=[product.slug]))


class ProductMarkDeletion(View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        if self.request.user.is_authenticated:
            product.set_deletion_mark()
        return HttpResponseRedirect(reverse_lazy('content:product', args=[product.slug]))


class ProductMarkImage(View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        if self.request.user.is_authenticated:
            product.set_image_update_mark()
        return HttpResponseRedirect(reverse_lazy('content:product', args=[product.slug]))


class ProductMarkCategory(View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        if self.request.user.is_authenticated:
            product.set_category_upate_mark()
        return HttpResponseRedirect(reverse_lazy('content:product', args=[product.slug]))


class ProductMarkText(View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        if self.request.user.is_authenticated:
            product.set_text_update_mark()
        return HttpResponseRedirect(reverse_lazy('content:product', args=[product.slug]))


class CiView(ContentView):
    template_name = 'qc_ci.html'
