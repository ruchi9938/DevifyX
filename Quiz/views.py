from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from datetime import datetime, timedelta
from django.db import models
import json
 
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'total_questions': QuesModel.objects.count(),
            'total_users': User.objects.count(),
            'total_attempts': QuizAttempt.objects.count(),
        }
        return render(request, 'Quiz/dashboard.html', context)
    return redirect('login')

@login_required
def quiz(request, category_id=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', [])
            
            if not answers:
                return JsonResponse({'error': 'No answers provided'}, status=400)
            
            print(f"Processing {len(answers)} answers")  # Debug log
            print(f"Raw answers data: {answers}")  # Debug log
            
            results = []
            correct_answers = 0
            incorrect_answers = 0
            total_score = 0
            
            for answer in answers:
                question_id = int(answer.get('question_id', 0))  # Convert to int and provide default
                selected_answer = str(answer.get('selected_answer', '')).strip()  # Convert to string and strip whitespace
                
                print(f"Processing answer for question {question_id}: {selected_answer}")  # Debug log
                
                if not question_id or not selected_answer:
                    print(f"Skipping invalid answer: {answer}")  # Debug log
                    continue
                
                question = QuesModel.objects.get(id=question_id)
                is_correct = selected_answer == question.ans
                
                print(f"Question found: {question.question}")  # Debug log
                print(f"Correct answer: {question.ans}, Selected: {selected_answer}")  # Debug log
                
                # Check if user has exceeded max attempts
                profile = request.user.userprofile
                attempts = QuizAttempt.objects.filter(user=request.user, question=question).count()
                
                if attempts >= profile.max_attempts:
                    print(f"Max attempts reached for question {question_id}")  # Debug log
                    continue
                
                # Create attempt record
                QuizAttempt.objects.create(
                    user=request.user,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                )
                
                # Update user profile
                if is_correct:
                    profile.total_score += question.points
                    profile.save()
                    total_score += question.points
                    correct_answers += 1
                    print(f"Correct answer! Added {question.points} points")  # Debug log
                else:
                    incorrect_answers += 1
                    print("Incorrect answer")  # Debug log
                
                results.append({
                    'question_number': len(results) + 1,
                    'question_text': question.question,
                    'selected_answer': selected_answer,
                    'correct_answer': question.ans,
                    'is_correct': is_correct
                })
            
            if not results:
                return JsonResponse({'error': 'No valid answers were processed'}, status=400)
            
            print(f"Successfully processed {len(results)} answers")  # Debug log
            print(f"Score: {total_score}, Correct: {correct_answers}, Incorrect: {incorrect_answers}")
            
            return JsonResponse({
                'score': total_score,
                'total_questions': len(answers),
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'results': results
            })
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")  # Debug log
            return JsonResponse({'error': 'Invalid request data'}, status=400)
        except QuesModel.DoesNotExist as e:
            print(f"Question not found: {str(e)}")  # Debug log
            return JsonResponse({'error': 'One or more questions not found'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug log
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    
    # Get questions based on category
    try:
        if category_id:
            questions = QuesModel.objects.filter(category_id=category_id)
        else:
            questions = QuesModel.objects.all()
        
        context = {
            'questions': questions,
            'categories': Category.objects.all(),
        }
        return render(request, 'Quiz/quiz.html', context)
    except Exception as e:
        print(f"Error loading questions: {str(e)}")  # Debug log
        return JsonResponse({'error': 'Error loading questions. Please try again.'}, status=500)
 
@login_required
def addQuestion(request):    
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_admin:
        messages.error(request, 'You do not have permission to add questions. Please contact an administrator.')
        return redirect('home')
    
    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('home')
    else: 
        form = addQuestionform()
    
    context = {'form': form}
    return render(request, 'Quiz/addQuestion.html', context)

@login_required
def addCategory(request):
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_admin:
        messages.error(request, 'You do not have permission to add categories. Please contact an administrator.')
        return redirect('home') 
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('home')
    else:
        form = CategoryForm()
    
    context = {'form': form}
    return render(request, 'Quiz/addCategory.html', context)
 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else: 
        form = createuserform()
    
    context = {'form': form}
    return render(request, 'Quiz/register.html', context)
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'Quiz/login.html')
 
def logoutPage(request):
    logout(request)
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
                
                # Print reset link to console instead of sending email
                print("\n" + "="*50)
                print("Password Reset Link:")
                print(reset_url)
                print("="*50 + "\n")
                
                messages.success(request, 'Password reset link has been generated. Please check the console.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email address.')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'Quiz/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now login with your new password.')
                return redirect('login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'Quiz/password_reset_confirm.html', {'form': form})
    
    messages.error(request, 'The password reset link is invalid or has expired.')
    return redirect('login')

@login_required
def user_profile(request):
    profile = request.user.userprofile
    attempts = QuizAttempt.objects.filter(user=request.user)
    context = {
        'profile': profile,
        'attempts': attempts,
        'total_questions': QuesModel.objects.count(),
        'correct_answers': attempts.filter(is_correct=True).count(),
    }
    return render(request, 'Quiz/profile.html', context)

@login_required
def admin_dashboard(request):
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('home')
    
    # Get statistics
    total_users = User.objects.count()
    total_questions = QuesModel.objects.count()
    total_attempts = QuizAttempt.objects.count()
    correct_attempts = QuizAttempt.objects.filter(is_correct=True).count()
    
    # Get recent activity
    recent_attempts = QuizAttempt.objects.select_related('user', 'question').order_by('-attempted_at')[:10]
    
    # Get category statistics
    category_stats = Category.objects.annotate(
        question_count=Count('questions'),
        attempt_count=Count('questions__quizattempt'),
        correct_count=Count('questions__quizattempt', filter=models.Q(questions__quizattempt__is_correct=True))
    )
    
    context = {
        'total_users': total_users,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'recent_attempts': recent_attempts,
        'category_stats': category_stats,
    }
    return render(request, 'Quiz/admin_dashboard.html', context)