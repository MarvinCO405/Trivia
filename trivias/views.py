from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Trivia, TriviaScore
import requests
import random
import html
from django.utils.timezone import now

def history(request):
    if request.user.is_authenticated:
        trivia_scores = TriviaScore.objects.filter(user=request.user).order_by('-last_played')
    else:
        trivia_scores = []

    return render(request, 'trivias/history.html', {'trivia_scores': trivia_scores})


def index(request):
    trivias=Trivia.objects.all()
    search_term = request.GET.get('search', '').strip()
    difficulty_filter = request.GET.get('difficulty', '')

    filtered_trivias = trivias
    if search_term:
        filtered_trivias = [t for t in trivias if search_term.lower() in t.name.lower()]
    if difficulty_filter:
        filtered_trivias = [t for t in filtered_trivias if t.difficulty.lower() == difficulty_filter.lower()]

    trivia_list = []
    for trivia in filtered_trivias:
        image_url = get_image_for_category(trivia.name)
        trivia_list.append({
            'id': trivia.id,
            'name': trivia.name,
            'difficulty': trivia.difficulty,
            'image_url': image_url
        })


    template_data = {}
    template_data['title'] = 'Trivias'
    template_data['trivias'] = trivia_list
    return render(request, 'trivias/index.html',
                  {'template_data': template_data, 'request': request})


def get_image_for_category(category):
    access_key = '6g3eHClcvIEYhQSEp0-Z0FG-vFoqSjhahwjirR0Qkes'
    unsplash_url = f"https://api.unsplash.com/photos/random?query={category}&client_id={access_key}"
    response = requests.get(unsplash_url)
    if response.status_code == 200:
        data = response.json()
        return data['urls']['regular']
    else:
        return None




def show(request, id):
    trivia = get_object_or_404(Trivia, id=id)


    response = requests.get(trivia.url)
    data = response.json()
    questions = data.get('results', [])

    for q in questions:
        q['question'] = html.unescape(q['question'])
        q['correct_answer'] = html.unescape(q['correct_answer'])
        q['incorrect_answers'] = [html.unescape(ans) for ans in q['incorrect_answers']]


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


        TriviaScore.objects.create(
            user=request.user,
            trivia=trivia,
            score=score,
            last_played=now()
        )

        return redirect('leaderboard', trivia_id=trivia_id)
    return redirect('trivias.index')


def leaderboard(request, trivia_id):
    trivia = get_object_or_404(Trivia, id=trivia_id)
    scores = TriviaScore.objects.filter(trivia=trivia).order_by('-score', '-last_played')[:10]
    return render(request, 'trivias/leaderboard.html', {'scores': scores, 'trivia': trivia})
