from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Profile, Trivia, TriviaScore
import requests
import random
import html

def index(request):
    trivias=Trivia.objects.all()
    search_term = request.GET.get('search', '').strip()
    difficulty_filter = request.GET.get('difficulty', '')

    filtered_trivias = trivias
    if search_term:
        filtered_trivias = [t for t in trivias if search_term.lower() in t.name.lower()]
    if difficulty_filter:
        filtered_trivias = [t for t in filtered_trivias if t.difficulty == difficulty_filter]

    template_data = {}
    template_data['title'] = 'Trivias'
    template_data['trivias'] = filtered_trivias
    return render(request, 'trivias/index.html',
                  {'template_data': template_data, 'request': request})

def show(request, id):
    trivia = get_object_or_404(Trivia, id=id)

    # Fetch trivia questions from the correct API
    response = requests.get(trivia.url)
    data = response.json()
    questions = data.get('results', [])

    for q in questions:
        q['question'] = html.unescape(q['question'])
        q['correct_answer'] = html.unescape(q['correct_answer'])
        q['incorrect_answers'] = [html.unescape(ans) for ans in q['incorrect_answers']]

    # Shuffles answers around
    for q in questions:
        q['answers'] = q['incorrect_answers'] + [q['correct_answer']]
        random.shuffle(q['answers'])

    trivia_questions = random.sample(questions, 16) if len(questions) >= 16 else questions

    user_score = None
    if request.user.is_authenticated:
        user_score = TriviaScore.objects.filter(user=request.user, trivia=trivia).first()

    template_data = {
        'title': trivia.name,
        'trivia': trivia,
        'trivia_questions': trivia_questions,
        'user_score': user_score

    }

    return render(request, 'trivias/show.html', template_data)

def save_score_and_redirect(request, trivia_id):
    if request.method == "POST" and request.user.is_authenticated:
        score = int(request.POST.get('score', 0))
        trivia = get_object_or_404(Trivia, id=trivia_id)

        # Create or update the TriviaScore
        user_score, created = TriviaScore.objects.get_or_create(user=request.user, trivia=trivia)

        # Only update if the score is higher or if it's the first time the user plays
        if score > user_score.score or created:
            user_score.score = score
            user_score.last_played = timezone.now()  # Update the last played time
            user_score.save()

        return redirect('leaderboard', trivia_id=trivia_id)  # Redirect to leaderboard
    return redirect('trivias.index')


def leaderboard(request, trivia_id):
    trivia = get_object_or_404(Trivia, id=trivia_id)
    scores = TriviaScore.objects.filter(trivia=trivia).order_by('-score')[:10]  # <--- fix model
    return render(request, 'trivias/leaderboard.html', {'scores': scores, 'trivia': trivia})

@login_required
def history(request):
    trivia_scores = TriviaScore.objects.filter(user=request.user).order_by('-last_played')  # Filter by trivia_id
    return render(request, 'trivias/history.html', {'trivia_scores': trivia_scores})