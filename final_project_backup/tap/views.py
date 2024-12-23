import os
import csv
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Post, Category, Tag, Region, RealTimeTomatoData, TomatoPost, Recipe
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Farm
from .forms import FarmForm
from django.core.exceptions import ObjectDoesNotExist


@login_required
def select_user_type(request):
    """
    회원 유형 선택 페이지: 사용자가 농가 회원 또는 일반 회원을 선택할 수 있도록 한다.
    """
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        if user_type == "farmer":
            # 농가 그룹 추가
            farmer_group, created = Group.objects.get_or_create(name="농가")
            request.user.groups.clear()  # 기존 그룹 제거
            request.user.groups.add(farmer_group)
            messages.success(request, "농가 회원으로 등록되었습니다.")
        elif user_type == "regular":
            # 일반 회원 그룹 추가
            regular_group, created = Group.objects.get_or_create(name="일반 회원")
            request.user.groups.clear()  # 기존 그룹 제거
            request.user.groups.add(regular_group)
            messages.success(request, "일반 회원으로 등록되었습니다.")

        return redirect('tap:index')

    return render(request, 'tap/select_user_type.html')


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')
    new_posts = Post.objects.order_by('-created_at')[:3]

    return render(request, 'tap/index.html',
                  {'title': 'TAP', 'posts': posts, 'categories': categories, 'new_posts': new_posts})


def post_detail(request, pk, slug):
    post = get_object_or_404(Post, pk=pk, slug=slug)
    categories = Category.objects.all()
    regions = Region.objects.all().order_by('name')
    region_posts = Post.objects.select_related('region').all()

    farm = None
    if post.author and hasattr(post.author, 'farm'):
        farm = post.author.farm

    return render(request, 'tap/post_detail.html',
                  {'title': post.title, 'post': post, 'categories': categories, 'regions': regions,
                   'region_posts': region_posts, 'farm': farm,})


def post_list(request):
    # 검색어 처리
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')
    regions = Region.objects.all().order_by('name')
    region_posts = Post.objects.select_related('region').all()
    if query:
        posts = posts.filter(
            Q(title__iexact=query) |
            Q(category__name__iexact=query) |
            Q(tags__name__iexact=query)
        ).distinct()

    # 페이지네이션 처리
    paginator = Paginator(posts, 6)  # 페이지당 12개
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # 카테고리와 태그 목록
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'tap/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'query': query,
        'regions': regions,
        'region_posts': region_posts
    })


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all().order_by('name')
    regions = Region.objects.all().order_by('name')
    region_posts = Post.objects.select_related('region').all()
    return render(request, 'tap/category_list.html',
                  {'posts': posts, 'categories': categories, 'category': category, 'regions': regions,
                   'region_posts': region_posts})


def tag_list(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = tag.post_set.all()
    region_posts = Post.objects.select_related('region').all()
    return render(request, 'tap/tag_list.html', {
        'posts': posts,
        'tag': tag,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'region_posts': region_posts
    })


class PostCreate(CreateView):
    model = Post
    fields = [
        'title',
        'region',
        'slug',
        'farm_owner',
        'content',
        'head_image',
        'file_upload',
        'category',
        'tags',
    ]
    success_url = reverse_lazy('tap:create_post')

def smartfarm_intro(request):
    """
    스마트팜 소개 페이지: 스마트팜에 대한 설명과 특징을 보여줍니다.
    """
    return render(request, 'tap/smartfarm_intro.html')

def recipe_detail(request, slug, pk):
    """
    손질 및 레시피 페이지
    """
    post = get_object_or_404(Post, slug=slug, pk=pk)
    recipes = Recipe.objects.filter(crop=post)

    return render(request, 'tap/recipe_detail.html', {
        'post': post,
        'recipes': recipes
    })

def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    owner_image = farm.owner_image.url if farm.owner_image else None
    print(farm.farm_slug)

    return render(request, 'tap/farm_info.html', {
        'farm': farm,
        'owner_image': owner_image,
    })

@login_required
def manage_farm(request):
    # 사용자와 연결된 농가 정보 가져오기
    farm, created = Farm.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # 파일 처리 포함
        form = FarmForm(request.POST, request.FILES, instance=farm)
        if form.is_valid():
            form.save()
            return redirect('tap:index')  # 저장 후 리다이렉트
    else:
        form = FarmForm(instance=farm)

    return render(request, 'tap/manage_farm.html', {'form': form, 'farm': farm})

def get_csv_data(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if not post.file_upload:
            return JsonResponse({"error": "CSV 파일이 없습니다."}, status=400)

        csv_file_path = post.file_upload.path
        df = pd.read_csv(csv_file_path)

        # 열 이름 정리
        df.columns = df.columns.str.strip()

        # 새로운 열 이름 검사
        required_columns = {'timestamp', 'temperature', 'humidity'}
        if not required_columns.issubset(df.columns):
            return JsonResponse({
                "error": f"CSV 파일의 열 이름: {', '.join(df.columns)}. 'timestamp', 'temperature', 'humidity' 열이 필요합니다."
            }, status=400)

        # 데이터 반환
        data = {
            "timestamp": df['timestamp'].tolist(),
            "temperature": df['temperature'].tolist(),
            "humidity": df['humidity'].tolist()
        }
        return JsonResponse(data)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post를 찾을 수 없습니다."}, status=404)

def render_saved_chart(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if not post.file_upload:
            return render(request, 'error.html', {"message": "CSV 파일이 없습니다."})

        # CSV 파일 읽기
        csv_file_path = post.file_upload.path
        df = pd.read_csv(csv_file_path)

        # 열 이름 정리
        df.columns = df.columns.str.strip()
        required_columns = {'timestamp', 'temperature', 'humidity'}
        if not required_columns.issubset(df.columns):
            return render(request, 'error.html', {"message": f"CSV 파일의 열 이름: {', '.join(df.columns)}. 'timestamp', 'temperature', 'humidity' 열이 필요합니다."})

        # 데이터 준비
        data = {
            "timestamp": df['timestamp'].tolist(),
            "temperature": df['temperature'].tolist(),
            "humidity": df['humidity'].tolist()
        }

        # saved_post_chart.html 템플릿 렌더링
        return render(request, 'tap/saved_post_chart.html', {
            "post": post,
            "chart_data": data
        })

    except Post.DoesNotExist:
        return render(request, 'error.html', {"message": "Post를 찾을 수 없습니다."})

def chart(request):
    posts = Post.objects.all()
    return render(request, 'tap/saved_post_chart.html', {'posts': posts})

# @csrf_exempt
# def receive_real_time_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             RealTimeTomatoData.objects.create(
#                 timestamp=data.get('timestamp', timezone.now()),
#                 temperature=data.get('temperature'),
#                 humidity=data.get('humidity')
#             )
#             return JsonResponse({"status": "success", "message": "Data saved successfully"})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
#     return JsonResponse({"status": "error", "message": "Invalid request method"})
#
#
# # 🟢 2. 실시간 데이터 차트 데이터 반환
# def real_time_chart_data(request):
#     data = RealTimeTomatoData.objects.order_by('-timestamp')[:100]
#     response_data = [
#         {
#             'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#             'temperature': entry.temperature,
#             'humidity': entry.humidity
#         }
#         for entry in reversed(data)
#     ]
#     return JsonResponse(response_data, safe=False)
#
# # 🟢 Post 저장 (작기 종료 시 데이터 저장)
# @csrf_exempt
# def end_season_and_save_csv(request):
#     if request.method != 'POST':
#         return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
#
#     data = RealTimeTomatoData.objects.all()
#     if not data.exists():
#         return JsonResponse({"status": "error", "message": "No data to save"})
#
#     try:
#         # 사용자 입력 받기
#         body = json.loads(request.body)
#         category = body.get('category', '일반')
#         title = body.get('title', '작기 종료')
#         content = body.get('content', '작기 종료 완료')
#
#         # CSV 파일 저장
#         filename = f"real_time_data_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
#         file_path = os.path.join(settings.MEDIA_ROOT, filename)
#
#         if not os.path.exists(settings.MEDIA_ROOT):
#             os.makedirs(settings.MEDIA_ROOT)
#
#         with open(file_path, mode='w', newline='', encoding='utf-8') as file_upload:
#             writer = csv.writer(file_upload)
#             writer.writerow(['timestamp', 'temperature', 'humidity'])
#             for entry in data:
#                 writer.writerow([entry.timestamp, entry.temperature, entry.humidity])
#
#         # Post 저장
#         Post.objects.create(
#             category=category,
#             title=title,
#             content=content,
#             file_upload=filename
#         )
#
#         # 데이터 초기화
#         data.delete()
#
#         return JsonResponse({
#             "status": "success",
#             "message": "Post saved, data reset, and CSV file created successfully.",
#             "filename": filename
#         })
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)})
#
#
# # 🟢 4. 실시간 데이터 그래프 페이지 렌더링
# def real_time_chart(request):
#     return render(request, 'tap/real_time_chart.html')
#
#
# # 🟢 5. 저장된 CSV 파일 선택 페이지 렌더링
# def saved_csv_chart(request):
#     file_upload = [f for f in os.listdir(settings.MEDIA_ROOT) if f.endswith('.csv')]
#     return render(request, 'tap/saved_csv_chart.html', {'file_upload': file_upload})
#
#
# # 🟢 6. 선택된 CSV 파일 데이터를 JSON으로 반환
# def saved_csv_chart_data(request):
#     selected_file = request.GET.get('file', '')
#
#     if not selected_file:
#         return JsonResponse({"status": "error", "message": "No file selected."}, status=400)
#
#     csv_file_path = os.path.join(settings.MEDIA_ROOT, selected_file)
#
#     if not os.path.exists(csv_file_path):
#         return JsonResponse({"status": "error", "message": "CSV 파일이 존재하지 않습니다."}, status=404)
#
#     data = []
#     try:
#         with open(csv_file_path, mode='r', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 data.append({
#                     'timestamp': row['timestamp'],
#                     'temperature': float(row['temperature']),
#                     'humidity': float(row['humidity'])
#                 })
#         return JsonResponse(data, safe=False)
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)
#
# # 🟢 CSV 그래프 페이지 렌더링
# def saved_post_chart(request):
#     posts = Post.objects.filter(file_upload__isnull=False)
#     return render(request, 'tap/saved_post_chart.html', {'posts': posts})
#
# # 🟢 선택된 Post의 CSV 데이터 반환
# def post_csv_chart_data(request):
#     post_id = request.GET.get('post_id')
#
#     if not post_id:
#         return JsonResponse({"status": "error", "message": "No post ID provided"}, status=400)
#
#     try:
#         post = get_object_or_404(Post, id=post_id)
#
#         if not post.csv_file:
#             return JsonResponse({"status": "error", "message": "No CSV file associated with this post"}, status=400)
#
#         csv_file_path = os.path.join(settings.MEDIA_ROOT, str(post.csv_file))
#
#         if not os.path.exists(csv_file_path):
#             return JsonResponse({"status": "error", "message": "CSV file does not exist"}, status=404)
#
#         data = []
#         with open(csv_file_path, mode='r', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 data.append({
#                     'timestamp': row['timestamp'],
#                     'temperature': float(row['temperature']),
#                     'humidity': float(row['humidity'])
#                 })
#
#         return JsonResponse(data, safe=False)
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)