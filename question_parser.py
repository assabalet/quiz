import random

def parse_questions(text):
    questions = []
    blocks = text.strip().split('\n\n')  # 空行で問題を区切る

    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue

        question_text = lines[0]
        options = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('+'):
                options.append({'text': line[1:].strip(), 'correct': True})
            elif line.startswith('-'):
                options.append({'text': line[1:].strip(), 'correct': False})
        
        random.shuffle(options)  # 選択肢をシャッフル
        questions.append({'text': question_text, 'options': options})

    return questions
