from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"),name="users"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('reservation/', include('reservation.urls')),

]
