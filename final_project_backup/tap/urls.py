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
    ]
    # 🟢 실시간 데이터 수신 (라즈베리파이 → Django)
#     path('save_data/', views.receive_real_time_data, name='receive_real_time_data'),
#
#     # 🟢 실시간 데이터 그래프 데이터 반환 (Chart.js 사용)
#     path('chart_data/', views.real_time_chart_data, name='real_time_chart_data'),
#
#     # 🟢 실시간 데이터 그래프 페이지
#     path('chart/', views.real_time_chart, name='real_time_chart'),
#
#     # 🟢 작기 종료: CSV 저장 및 데이터 초기화
#     path('end_season/', views.end_season_and_save_csv, name='end_season'),
#
#     # 🟢 선택된 CSV 파일 데이터 반환
#     path('saved_csv_chart_data/', views.saved_csv_chart_data, name='saved_csv_chart_data'),
#     path('saved_post_chart/', views.saved_post_chart, name='saved_post_chart'),
#     path('post_csv_chart_data/', views.post_csv_chart_data, name='post_csv_chart_data'),
# ]

    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path("detail/<int:pk>/", post_detail, name="post_detail"),
#     path('category/<slug:slug>/', views.category_detail, name='category_detail'),
#     path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
#     path('create_post/', views.PostCreate.as_view(), name='create_post'),
#     path('update_post/<int:pk>', views.PostUpdate.as_view(), name='post_update'),