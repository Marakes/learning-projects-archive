from django.urls import include, path

urlpatterns = [
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
]
