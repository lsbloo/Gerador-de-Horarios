from django.urls import path
from . import views
from django.conf.urls import url

app_name="kitkat"

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/',views.painel,name='dashboard'),
    path('dashboard/user',views.painel_user,name='dashboard_usuario'),
    path('dashboard/users/',views.painel_users,name="dashboard_user"),
    url('dashboardc/(?P<slug>[\w\-]+)',views.painelc,name='dashboardc'),
    url(r'^generate/', views.generate, name="generate-criterio"),
    url(r'^create/user/',views.generate_user,name="generate-user"),
    url(r'^criterio/(?P<pk>[0-9]+)/$', views.remove_criterio,name="remove_criterio"),
    url(r'^criterio/edt/(?P<pk>[0-9]+)/$', views.edit_criterio ,name="edit_criterio"),
    url(r'^criterio/edt/p/(?P<pk>[0-9]+)/$',views.edit_criterio_p,name="edit_criterio_p"),
    url(r'^user/delete/(?P<pk>[0-9]+)/$',views.delete_user,name="delete_user")

    

]
