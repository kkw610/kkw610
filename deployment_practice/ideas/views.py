from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Idea, DevTool

# Create your views here.
def ideas_list(request):
    """아이디어 목록 페이지 (기능1, 2, 3, 4)"""
    # 정렬 옵션
    sort = request.GET.get('sort', '-created_at')
    search = request.GET.get('search', '')
    
    # 기본 쿼리셋
    ideas = Idea.objects.all()
    
    # 검색 기능
    if search:
        ideas = ideas.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(devtool__name__icontains=search)
        )
    
    # 정렬
    sort_options = {
        'star': '-star_count',
        'title': 'title',
        'created': 'created_at',
        '-created': '-created_at',
        'interest': '-interest',
    }
    
    if sort in sort_options:
        ideas = ideas.order_by(sort_options[sort])
    else:
        ideas = ideas.order_by('-created_at')
    
    # 페이지네이션 (챌린지: 4개씩)
    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 세션에서 찜한 아이디어 확인
    starred_ideas = request.session.get('starred_ideas', [])
    for idea in page_obj:
        idea.is_starred = idea.pk in starred_ideas
    
    context = {
        'page_obj': page_obj,
        'sort': sort,
        'search': search,
    }
    return render(request, 'ideas_list.html', context)


def ideas_create(request):
    """아이디어 등록 페이지 (기능5)"""
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        interest = request.POST.get('interest', 0)
        devtool_id = request.POST.get('devtool')
        
        idea = Idea.objects.create(
            title=title,
            image=image,
            content=content,
            interest=interest,
            devtool_id=devtool_id,
        )
        return redirect('ideas:ideas_detail', pk=idea.pk)
    
    devtools = DevTool.objects.all()
    return render(request, 'ideas_form.html', {'devtools': devtools})


def ideas_detail(request, pk):
    """아이디어 상세 페이지 (기능6, 7, 8)"""
    idea = Idea.objects.get(pk=pk)
    
    # 세션에서 찜 여부 확인
    starred_ideas = request.session.get('starred_ideas', [])
    is_starred = idea.pk in starred_ideas
    
    context = {
        'idea': idea,
        'is_starred': is_starred,
    }
    return render(request, 'ideas_detail.html', context)


def ideas_update(request, pk):
    """아이디어 수정 페이지 (기능9)"""
    idea = Idea.objects.get(pk=pk)
    
    if request.method == 'POST':
        idea.title = request.POST.get('title')
        if request.FILES.get('image'):
            idea.image = request.FILES.get('image')
        idea.content = request.POST.get('content')
        idea.interest = request.POST.get('interest', 0)
        idea.devtool_id = request.POST.get('devtool')
        idea.save()
        return redirect('ideas:ideas_detail', pk=idea.pk)
    
    devtools = DevTool.objects.all()
    context = {
        'idea': idea,
        'devtools': devtools,
    }
    return render(request, 'ideas_form.html', context)


def ideas_delete(request, pk):
    """아이디어 삭제 (기능7)"""
    idea = Idea.objects.get(pk=pk)
    if request.method == 'POST':
        idea.delete()
        return redirect('ideas:ideas_list')
    return redirect('ideas:ideas_detail', pk=pk)


def ideas_star_toggle(request, pk):
    """아이디어 찜하기 토글 (AJAX, 세션 기반) (기능3, 8, 챌린지)"""
    if request.method == 'POST':
        idea = Idea.objects.get(pk=pk)
        
        # 세션에서 찜한 아이디어 목록 가져오기
        starred_ideas = request.session.get('starred_ideas', [])
        
        if idea.pk in starred_ideas:
            # 찜 취소
            starred_ideas.remove(idea.pk)
            idea.star_count -= 1
            is_starred = False
        else:
            # 찜 추가
            starred_ideas.append(idea.pk)
            idea.star_count += 1
            is_starred = True
        
        request.session['starred_ideas'] = starred_ideas
        idea.save()
        
        return JsonResponse({
            'is_starred': is_starred,
            'star_count': idea.star_count,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def ideas_interest_increase(request, pk):
    """관심도 증가 (AJAX) (기능4, 챌린지)"""
    if request.method == 'POST':
        idea = Idea.objects.get(pk=pk)
        idea.interest += 1
        idea.save()
        return JsonResponse({'interest': idea.interest})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def ideas_interest_decrease(request, pk):
    """관심도 감소 (AJAX) (기능4, 챌린지)"""
    if request.method == 'POST':
        idea = Idea.objects.get(pk=pk)
        if idea.interest > 0:
            idea.interest -= 1
            idea.save()
        return JsonResponse({'interest': idea.interest})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 개발툴 관련 Views
def devtools_list(request):
    """개발툴 목록 페이지 (기능10)"""
    devtools = DevTool.objects.all().order_by('-created_at')
    
    # 페이지네이션 (4개씩)
    paginator = Paginator(devtools, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'devtools_list.html', context)


def devtools_create(request):
    """개발툴 등록 페이지 (기능11)"""
    if request.method == 'POST':
        name = request.POST.get('name')
        kind = request.POST.get('kind')
        content = request.POST.get('content')
        
        devtool = DevTool.objects.create(
            name=name,
            kind=kind,
            content=content,
        )
        return redirect('ideas:devtools_detail', pk=devtool.pk)
    
    return render(request, 'devtools_form.html', {'KIND_CHOICES': DevTool.KIND_CHOICES})


def devtools_detail(request, pk):
    """개발툴 상세 페이지 (기능12, 13)"""
    devtool = DevTool.objects.get(pk=pk)
    ideas = devtool.ideas.all()
    
    context = {
        'devtool': devtool,
        'ideas': ideas,
    }
    return render(request, 'devtools_detail.html', context)


def devtools_update(request, pk):
    """개발툴 수정 페이지 (기능14)"""
    devtool = DevTool.objects.get(pk=pk)
    
    if request.method == 'POST':
        devtool.name = request.POST.get('name')
        devtool.kind = request.POST.get('kind')
        devtool.content = request.POST.get('content')
        devtool.save()
        return redirect('ideas:devtools_detail', pk=devtool.pk)
    
    context = {
        'devtool': devtool,
        'KIND_CHOICES': DevTool.KIND_CHOICES,
    }
    return render(request, 'devtools_form.html', context)


def devtools_delete(request, pk):
    """개발툴 삭제 (기능13)"""
    devtool = DevTool.objects.get(pk=pk)
    if request.method == 'POST':
        devtool.delete()
        return redirect('ideas:devtools_list')
    return redirect('ideas:devtools_detail', pk=pk)