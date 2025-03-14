import csv
import re

def parse_question(line):
    # 使用正則表達式解析題目格式
    match = re.match(r"(\d+)\. \((.)\) (.*?) \(A\)(.*?) \(B\)(.*?) \(C\)(.*?) \(D\)(.*)", line)
    if match:
        q_id, correct_answer, question, option_a, option_b, option_c, option_d = match.groups()
        return [q_id.strip(), question.strip(), option_a.strip(), option_b.strip(), option_c.strip(), option_d.strip(), correct_answer.strip()]
    return None

def process_questions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["id", "question", "option_A", "option_B", "option_C", "option_D", "correct_answer"])
        
        for line in infile:
            parsed = parse_question(line.strip())
            if parsed:
                csv_writer.writerow(parsed)
    print(f"✅ 資料處理完成，已儲存至 {output_file}")

# 使用範例
process_questions("questions.txt", "questions.csv")
