from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']  # Ajout des filtres
    search_fields = ['title', 'body']  # Champs de recherche
    prepopulated_fields = {'slug': ('title',)}  # Pré-remplir slug avec le titre
    raw_id_fields = ['author']  # Widget de recherche pour auteur
    date_hierarchy = 'publish'  # Hiérarchie de dates
    ordering = ['status', 'publish']  # Critères de tri par défaut
    show_facets = admin.ShowFacets.ALWAYS
