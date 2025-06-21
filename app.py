from flask import Flask, render_template, request, redirect, url_for, session
from question_parser import parse_questions
import random
 import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 最大5MBまでのアップロード許可

# グローバル変数（本番環境ではDB等にすべき）
QUESTIONS = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        файл = request.files['file']
        if файл:
            try:
                содержимое = файл.read().decode('utf-8', errors='ignore')
                global QUESTIONS
                QUESTIONS = parse_questions(содержимое)
                random.shuffle(QUESTIONS)  # 質問順をシャッフル
                session['answers'] = {}
                return redirect(url_for('quiz', qid=0))
            except Exception as e:
                return f"Ошибка при обработке файла: {e}"
    return render_template('index.html')

@app.route('/quiz/<int:qid>', methods=['GET', 'POST'])
def quiz(qid):
    global QUESTIONS
    if 'answers' not in session or qid >= len(QUESTIONS):
        return redirect(url_for('result'))

    вопрос = QUESTIONS[qid]
    выбранный = None
    правильно = None

    if request.method == 'POST':
        выбранный = request.form.get('answer')
        session['answers'][str(qid)] = выбранный
        session.modified = True

        правильные_ответы = [opt['text'] for opt in вопрос['options'] if opt['correct']]
        правильно = выбранный in правильные_ответы

        return render_template('quiz.html', qid=qid, question=вопрос, total=len(QUESTIONS),
                               selected=выбранный, is_correct=правильно)

    return render_template('quiz.html', qid=qid, question=вопрос, total=len(QUESTIONS))

@app.route('/result')
def result():
    global QUESTIONS
    правильных = 0
    ответы = session.get('answers', {})

    for i, q in enumerate(QUESTIONS):
        выбранный = ответы.get(str(i))
        правильные_ответы = [opt['text'] for opt in q['options'] if opt['correct']]
        if выбранный in правильные_ответы:
            правильных += 1

    всего = len(QUESTIONS)
    return render_template('result.html', correct=правильных, total=всего)

if __name__ == '__main__':
    app.run(debug=True)
   

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render が動的に割り当てるポート
    app.run(host='0.0.0.0', port=port)

