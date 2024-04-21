from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = 'your secret key'

lessons = [
    {"id": 1, "title": "Introduction to List Comprehensions"},
    {"id": 2, "title": "Video Examples"},
    {"id": 3, "title": "Easier Video Example"},
    {"id": 4, "title": "Harder Video Example"},
    {"id": 5, "title": "Coding Examples"},
    {"id": 6, "title": "Easy Coding Example"},
    {"id": 7, "title": "Hard Coding Example"}
]

CORRECT_ANSWERS = {
    'part1': 'B',
    'part2': {
        'droppable-uppercase': 'draggable-string',
        'droppable-numbers': 'draggable-array',
        'droppable-even-squares': 'draggable-even'
    },
    'part3': 'short_fruits = [fruit.upper() for fruit in fruits if len(fruit) < 6]'
}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/video-examples')
def video_examples():
    return render_template('video_examples.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    lesson = next((lesson for lesson in lessons if lesson["id"] == lesson_id), None)
    if lesson is None:
        return "Lesson not found", 404
    return render_template('learn.html', lesson=lesson)

@app.route('/easier-video-example')
def easier_video_example():
    return render_template('easy_video_example.html')

@app.route('/harder-video-example')
def harder_video_example():
    return render_template('hard_video_example.html')

@app.route('/quiz/<int:lesson_id>')
def quiz(lesson_id):
    pass

@app.route('/coding-examples')
def coding_examples():
    return render_template('coding_examples.html')

@app.route('/easy-coding-example')
def easy_coding_example():
    lesson = next((lesson for lesson in lessons if lesson["title"] == "Easy Coding Example"), None)
    return render_template('easy_coding_example.html', lesson=lesson)

@app.route('/hard-coding-example')
def hard_coding_example():
    lesson = next((lesson for lesson in lessons if lesson["title"] == "Hard Coding Example"), None)
    return render_template('hard_coding_example.html', lesson=lesson)

@app.route('/take-quiz')
def take_quiz():
    session['score'] = 0
    session['user_answers'] = {}
    return render_template('quiz_part_1.html')

@app.route('/quiz/part1', methods=['GET', 'POST'])
def quiz_part1():
    if request.method == 'POST':
        user_answer = request.form.get('question1')
        session['user_answers']['part1'] = user_answer
        if user_answer == CORRECT_ANSWERS['part1']:
            session['score'] += 33.3
        return redirect(url_for('take_quiz2'))
    return render_template('quiz_part_1.html')

@app.route('/take-quiz2')
def take_quiz2():
    return render_template('quiz_part_2.html')

@app.route('/quiz/part2', methods=['POST'])
def quiz_part2():
    data = request.get_json()
    session['user_answers']['part2'] = data
    if not data:
        return jsonify({'error': 'No data received'}), 400
    score_increment = 33.3 / len(CORRECT_ANSWERS['part2'])
    for key, value in data.items():
        if value == CORRECT_ANSWERS['part2'][key]:
            session['score'] += score_increment
    return jsonify({'score': session['score']})

@app.route('/quiz/part3', methods=['GET'])
def quiz_part3():
    return render_template('quiz_part_3.html')

@app.route('/submit-quiz-part3', methods=['POST'])
def submit_quiz_part3():
    user_input = request.form.get('code_answer', '').strip()
    normalized_user_input = ''.join(user_input.split()).upper()
    normalized_correct_answer = ''.join(CORRECT_ANSWERS['part3'].split()).upper()
    session['user_answers']['part3'] = user_input
    if normalized_user_input == normalized_correct_answer:
        session['score'] += 33.3
    session['passed'] = session['score'] >= 60
    return redirect(url_for('quiz_results'))

@app.route('/quiz-results')
def quiz_results():
    score = session.get('score', 0)
    passed = session.get('passed', False)
    user_answers = session.get('user_answers', {})
    normalized_correct_answers = {
        'part1': CORRECT_ANSWERS['part1'],
        'part2': {k: v for k, v in CORRECT_ANSWERS['part2'].items()},
        'part3': ''.join(CORRECT_ANSWERS['part3'].split())
    }
    normalized_user_answers = {
        'part1': user_answers.get('part1', ''),
        'part2': user_answers.get('part2', {}),
        'part3': ''.join(user_answers.get('part3', '').split())
    }
    results = {
        'part1': 'correct' if normalized_user_answers['part1'] == normalized_correct_answers['part1'] else 'incorrect',
        'part2': {k: 'correct' if normalized_user_answers['part2'].get(k, '') == v else 'incorrect' for k, v in normalized_correct_answers['part2'].items()},
        'part3': 'correct' if normalized_user_answers['part3'] == normalized_correct_answers['part3'] else 'incorrect'
    }
    return render_template(
        'quiz_results.html',
        score=score,
        passed=passed,
        user_answers=normalized_user_answers,
        results=results,
        correct_answers=normalized_correct_answers
    )

if __name__ == '__main__':
    app.run(debug=True)
