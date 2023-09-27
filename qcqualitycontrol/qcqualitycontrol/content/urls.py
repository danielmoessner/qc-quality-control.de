from django.urls import path

from . import views


app_name = "content"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('company-profile', views.CompanyProfileView.as_view(), name='companyprofile'),
    path('certificates', views.CertificatesView.as_view(), name='certificates'),
    path('products-search/', views.ProductsSearchView.as_view(), name='products_search'),
    path('products/<slug>', views.ProductsView.as_view(), name='products'),
    path('product/<slug>', views.ProductView.as_view(), name='product'),
    path('file/<slug>', views.FileView.as_view(), name='file'),
    path('product/<slug>/mark/deletion', views.ProductMarkDeletion.as_view(), name='productmarkdeletion'),
    path('product/<slug>/mark/image', views.ProductMarkImage.as_view(), name='productmarkimage'),
    path('product/<slug>/mark/category', views.ProductMarkCategory.as_view(), name='productmarkcategory'),
    path('product/<slug>/mark/text', views.ProductMarkText.as_view(), name='productmarktext'),
    path('ci', views.CiView.as_view(), name='ci')
]
