from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from django.contrib.auth import views as auth_views

app_name = 'tap'
urlpatterns = [
    path("", views.index, name="index"),
    path('farm/manage/', views.manage_farm, name='manage_farm'),
    path('create_post/', views.PostCreate.as_view(), name="create_post"),
    path("select_user_type/", views.select_user_type, name="select_user_type"),
    path('post/<slug:slug>/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('tag/<slug:slug>/', views.tag_list, name='tag_list'),
    path('account/', include('allauth.urls')),
    path('post/<int:post_id>/csv-data/', views.get_csv_data, name='get_csv_data'),
    path('post/<int:post_id>/chart/', views.render_saved_chart, name='saved_post_chart'),
    path('smartfarm_intro/', views.smartfarm_intro, name='smartfarm_intro'),
    path('recipe/<slug:slug>/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('farm/<int:pk>/', views.farm_detail, name='farm_detail'),
    path('save_data/', views.receive_real_time_data, name='receive_real_time_data'),
    path('chart/', views.real_time_chart, name='real_time_chart'),
    path('chart_data/', views.fetch_sensor_data, name='chart_data'),
    ]