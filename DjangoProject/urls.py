"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard principal
    path("", views.index, name="index"),

    # Usuarios
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:user_id>/", views.detalle_usuario, name="detalle_usuario"),

    # Canciones
    path("canciones/", views.lista_canciones, name="lista_canciones"),
    path("canciones/crear/", views.crear_cancion, name="crear_cancion"),
    path("canciones/<int:song_id>/", views.detalle_cancion, name="detalle_cancion"),

    # Géneros
    path("generos/", views.lista_generos, name="lista_generos"),
    path("generos/crear/", views.crear_genero, name="crear_genero"),

    # Playlists
    path("playlists/", views.lista_playlists, name="lista_playlists"),
    path("playlists/crear/", views.crear_playlist, name="crear_playlist"),
    path("playlists/<int:playlist_id>/", views.detalle_playlist, name="detalle_playlist"),

    # Comentarios
    path("comentarios/", views.lista_comentarios, name="lista_comentarios"),

    # Estadísticas
    path("estadisticas/", views.estadisticas, name="estadisticas"),

    # Vistas de Oracle optimizadas
    path("vistas/canciones/", views.canciones_completas, name="canciones_completas"),
    path("vistas/playlists/", views.playlists_publicas, name="playlists_publicas"),
    path("vistas/ranking/", views.ranking_canciones, name="ranking_canciones"),
    path("vistas/perfiles/", views.perfiles_usuarios, name="perfiles_usuarios"),
    path("vistas/perfiles/<int:user_id>/", views.perfil_usuario_detalle, name="perfil_usuario_detalle"),
]
