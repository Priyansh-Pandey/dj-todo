from django.urls import path

from . import views

urlpatterns = [
    path("",views.userhome),
    path("searchproduct/",views.searchproduct),
    path("searchsubcat/",views.searchsubcat),
    path("addproduct/",views.addproduct),
    path("fetchSubCategoryAJAX/",views.fetchSubCategoryAJAX),
    path("productlist/",views.productlist),
    path("funds/",views.funds),
    path("payment/",views.payment),
    path("success/",views.success),
    path("cancel/",views.cancel)
]
