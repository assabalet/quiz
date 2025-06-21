from docx import Document

def convert_docx_to_questions(docx_path, output_path):
    doc = Document(docx_path)
    questions = []
    current_question = []

    for para in doc.paragraphs:
        line = para.text.strip()
        if not line:
            if current_question:
                questions.append(current_question)
                current_question = []
        else:
            current_question.append(line)

    if current_question:
        questions.append(current_question)

    with open(output_path, 'w', encoding='utf-8') as f:
        for q in questions:
            for line in q:
                f.write(line.strip() + '\n')
            f.write('\n')  # 問題ごとの区切り

    print(f"変換完了: {output_path}")

# 実行部分
if __name__ == '__main__':
    convert_docx_to_questions('test.docx', 'questions.txt')
