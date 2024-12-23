from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@receiver(user_signed_up)
def assign_default_group_and_redirect(request, user, **kwargs):
    """
    회원가입 후 기본 그룹을 할당하고,
    회원 유형 선택 페이지로 리다이렉트.
    """
    # 기본 그룹 '일반 회원' 추가
    group, created = Group.objects.get_or_create(name="일반 회원")
    user.groups.add(group)

    # 리다이렉트 URL 반환
    return redirect('tap:select_user_type')


# 추가적으로 회원 유형 선택에 따라 권한을 부여하는 로직

@login_required
def select_user_type(request):
    """
    회원 유형 선택 페이지: 사용자가 농가 회원 또는 일반 회원을 선택할 수 있도록 한다.
    """
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        if user_type == "farmer":
            # 농가 그룹 가져오기 또는 생성
            farmer_group, created = Group.objects.get_or_create(name="농가")

            # 농가 그룹에 필요한 권한 추가
            add_post_permission = Permission.objects.get(codename="add_post", content_type__app_label="blog")
            change_post_permission = Permission.objects.get(codename="change_post", content_type__app_label="blog")
            farmer_group.permissions.add(add_post_permission, change_post_permission)

            # 사용자 그룹 업데이트
            request.user.groups.clear()  # 기존 그룹 제거
            request.user.groups.add(farmer_group)

            # 성공 메시지
            messages.success(request, "농가 회원으로 등록되었습니다.")

        elif user_type == "regular":
            # 일반 회원 그룹 가져오기 또는 생성
            regular_group, created = Group.objects.get_or_create(name="일반 회원")
            request.user.groups.clear()  # 기존 그룹 제거
            request.user.groups.add(regular_group)

            # 성공 메시지
            messages.success(request, "일반 회원으로 등록되었습니다.")

        # 회원 유형 선택 후 메인 페이지로 리다이렉트
        return redirect('tap:index')

    # GET 요청 처리: 회원 유형 선택 페이지 렌더링
    return render(request, 'tap/select_user_type.html')
