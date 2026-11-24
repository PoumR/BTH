from django.urls import path
from .views import CreateInscriptionView, ListeUsersView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- Auth ---
    path("login/", views.InscriptionView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    # --- Changement de mot de passe (utilisé par votre flag must_change_password) ---
    path(
        "password_change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html",
        ),
        name="password_change_done",
    ),
    # --- Réinitialisation par email (mot de passe oublié) ---
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),



    # =========================================================================
    path("accueil", views.hello_world, name="hello_world"),
    path("liste_emprunteur", ListeUsersView.as_view(), name="liste_users"),
    path("inscription", CreateInscriptionView.as_view(), name="creer_users"),
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(template_name="registration/login.html"),
    #     name="login",
    # ),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path(
    #     "password_reset/",
    #     auth_views.PasswordResetView.as_view(
    #         template_name="registration/password_reset_form.html",
    #     ),
    #     name="password_reset",
    # ),
    # path(
    #     "password_reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(
    #         template_name="registration/password_reset_done.html",
    #     ),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(
    #         template_name="registration/password_reset_confirm.html",
    #     ),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     auth_views.PasswordResetCompleteView.as_view(
    #         template_name="registration/password_reset_complete.html",
    #     ),
    #     name="password_reset_complete",
    # ),
]
