from django.shortcuts import render
import requests
import random
import re
trivias = [
    {'id' : 1, 'name' : 'Sports'},
    {'id' : 2, 'name' : 'Movies'}
]

def index(request):
    template_data = {}
    template_data['title'] = 'Trivias'
    template_data['trivias'] = trivias
    return render(request, 'trivias/index.html',
                  {'template_data': template_data})




def show(request, id):
    # Define trivia categories and their corresponding API URLs.
    trivias = [
        {'id': 1, 'name': 'Sports', 'api_url': "https://opentdb.com/api.php?amount=50&category=21&difficulty=medium&type=multiple"},
        {'id': 2, 'name': 'Movies', 'api_url': "https://opentdb.com/api.php?amount=50&category=11&type=multiple"}
    ]

    # Get the selected trivia
    trivia = next((t for t in trivias if t["id"] == id), None)

    if not trivia:
        return render(request, 'trivias/error.html', {'message': 'Trivia category not found.'})

    # Fetch trivia questions from the correct API
    response = requests.get(trivia['api_url'])
    data = response.json()
    questions = data.get('results', [])


    trivia_questions = random.sample(questions, 16)

    template_data = {
        'title': trivia['name'],
        'trivia': trivia,
        'trivia_questions': trivia_questions

    }

    return render(request, 'trivias/show.html', template_data)
