from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import WordsBank, WordType, DifficultyLevel, WordList, UserProfile, WordRelationship
from .forms import WordForm

def home(request):
    if request.user.is_authenticated:
        return redirect('vocabulary:dashboard')
    return render(request, 'vocabulary/home.html')

@login_required
def word_list(request):
    query = request.GET.get('q', '')
    words = WordsBank.objects.select_related('word_type', 'difficulty_level').all()
    
    if query:
        words = words.filter(
            Q(word__icontains=query) |
            Q(meaning_english__icontains=query) |
            Q(meaning_urdu__icontains=query)
        )
    
    words = words.order_by('word')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 20, 50]:
            per_page = 10
    except (ValueError, TypeError):
        per_page = 10
    
    paginator = Paginator(words, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vocabulary/word_list.html', {
        'page_obj': page_obj,
        'query': query,
        'total_words': words.count(),
        'per_page': per_page
    })

@login_required
def flashcard_view(request):
    query = request.GET.get('q', '')
    words = WordsBank.objects.select_related('word_type', 'difficulty_level').all()
    
    if query:
        words = words.filter(
            Q(word__icontains=query) |
            Q(meaning_english__icontains=query) |
            Q(meaning_urdu__icontains=query)
        )
    
    words = words.order_by('word')
    return render(request, 'vocabulary/flashcard.html', {'words': words, 'query': query})

@login_required
def dashboard(request):
    total_words = WordsBank.objects.count()
    word_types = WordType.objects.all()
    difficulty_levels = DifficultyLevel.objects.all()
    recent_words = WordsBank.objects.order_by('-created_at')[:5]
    
    context = {
        'total_words': total_words,
        'word_types': word_types,
        'difficulty_levels': difficulty_levels,
        'recent_words': recent_words,
    }
    return render(request, 'vocabulary/dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_words = WordsBank.objects.count()
    word_types = WordType.objects.all()
    difficulty_levels = DifficultyLevel.objects.all()
    word_lists = WordList.objects.all()
    recent_words = WordsBank.objects.order_by('-created_at')[:5]
    
    return render(request, 'vocabulary/admin_dashboard.html', {
        'total_words': total_words,
        'word_types': word_types,
        'difficulty_levels': difficulty_levels,
        'word_lists': word_lists,
        'recent_words': recent_words
    })

@user_passes_test(lambda u: u.is_staff)
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Word added successfully!')
            return redirect('vocabulary:admin_dashboard')
    else:
        form = WordForm()
    
    word_types = WordType.objects.all().order_by('word_type')
    difficulty_levels = DifficultyLevel.objects.all().order_by('level')
    word_lists = WordList.objects.all().order_by('word_list_name')
    
    return render(request, 'vocabulary/add_word.html', {
        'form': form,
        'word_types': word_types,
        'difficulty_levels': difficulty_levels,
        'word_lists': word_lists
    })

@user_passes_test(lambda u: u.is_staff)
def edit_word(request, word_id):
    word = get_object_or_404(WordsBank, id=word_id)
    
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            messages.success(request, 'Word updated successfully!')
            return redirect('vocabulary:admin_dashboard')
    else:
        form = WordForm(instance=word)
    
    return render(request, 'vocabulary/edit_word.html', {'form': form, 'word': word})

@user_passes_test(lambda u: u.is_staff)
def user_management(request):
    query = request.GET.get('q', '')
    users = User.objects.select_related().all()
    
    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    users = users.order_by('-date_joined')
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vocabulary/user_management.html', {
        'page_obj': page_obj,
        'query': query,
        'total_users': users.count()
    })

@user_passes_test(lambda u: u.is_staff)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_staff = 'is_staff' in request.POST
        user.save()
        
        profile.subscription_status = request.POST.get('subscription_status', 'free')
        profile.save()
        
        messages.success(request, f'User {user.email} updated successfully!')
        return redirect('vocabulary:user_management')
    
    return render(request, 'vocabulary/edit_user.html', {'user': user, 'profile': profile})

@user_passes_test(lambda u: u.is_staff)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = 'activated' if user.is_active else 'blocked'
    messages.success(request, f'User {user.email} has been {status}!')
    return redirect('vocabulary:user_management')

@user_passes_test(lambda u: u.is_staff)
def manage_categories(request):
    word_types = WordType.objects.all().order_by('word_type')
    difficulty_levels = DifficultyLevel.objects.all().order_by('level')
    word_lists = WordList.objects.all().order_by('word_list_name')
    
    return render(request, 'vocabulary/manage_categories.html', {
        'word_types': word_types,
        'difficulty_levels': difficulty_levels,
        'word_lists': word_lists
    })

@user_passes_test(lambda u: u.is_staff)
def add_word_type(request):
    if request.method == 'POST':
        word_type = request.POST.get('word_type')
        abbreviation = request.POST.get('abbreviation')
        if word_type:
            WordType.objects.create(word_type=word_type, abbreviation=abbreviation)
            messages.success(request, f'Word type "{word_type}" added successfully!')
    return redirect('vocabulary:manage_categories')

@user_passes_test(lambda u: u.is_staff)
def add_difficulty(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        if level:
            DifficultyLevel.objects.create(level=level)
            messages.success(request, f'Difficulty level "{level}" added successfully!')
    return redirect('vocabulary:manage_categories')

@user_passes_test(lambda u: u.is_staff)
def add_word_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            WordList.objects.create(word_list_name=name, description=description)
            messages.success(request, f'Word list "{name}" added successfully!')
    return redirect('vocabulary:manage_categories')

@user_passes_test(lambda u: u.is_staff)
def word_relationships(request):
    relationships = WordRelationship.objects.select_related('word1', 'word2').all().order_by('-created_at')
    paginator = Paginator(relationships, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vocabulary/word_relationships.html', {
        'page_obj': page_obj,
        'total_relationships': relationships.count()
    })

@user_passes_test(lambda u: u.is_staff)
def add_relationship(request):
    if request.method == 'POST':
        word1_id = request.POST.get('word1')
        word2_id = request.POST.get('word2')
        relationship_type = request.POST.get('relationship_type')
        
        if word1_id and word2_id and relationship_type:
            try:
                word1 = WordsBank.objects.get(id=word1_id)
                word2 = WordsBank.objects.get(id=word2_id)
                
                if relationship_type == 'synonym':
                    word1.add_synonym(word2)
                elif relationship_type == 'antonym':
                    word1.add_antonym(word2)
                
                messages.success(request, f'{relationship_type.title()} relationship added between "{word1.word}" and "{word2.word}"!')
            except WordsBank.DoesNotExist:
                messages.error(request, 'One or both words not found!')
    
    return redirect('vocabulary:word_relationships')