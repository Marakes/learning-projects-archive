from django.urls import include, path

from . import views


app_name = 'blog'

posts_urls = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('create/',
         views.PostCreateView.as_view(), name='create_post'),
    path('<int:post_id>/comment/',
         views.add_comment, name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]

urlpatterns = [
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('posts/', include(posts_urls)),
    path('profile/<str:profile_slug>/',
         views.ProfileView.as_view(), name='profile'),
    path('edit_profile/',
         views.EditProfileView.as_view(), name='edit_profile'),
    path('', views.index, name='index'),
]
