import csv
import re

def is_complete_question(text):
    """
    檢查 text 是否包含題號、答案以及所有選項標記
    """
    # 必須以題號開始，例如 "1."
    if not re.search(r'^\d+\.', text):
        return False
    # 檢查第一個括號是答案，例如 "1. (B)"
    if not re.search(r'^\d+\.\s*\([A-D]\)', text):
        return False
    # 檢查是否包含所有選項標記 (A)、(B)、(C)、(D)
    for token in ["(A)", "(B)", "(C)", "(D)"]:
        if token not in text:
            return False
    return True

def parse_question(text):
    """
    解析完整題目文字，格式預設為:
    題號. (答案) 題目文字 ... (A)選項文字 ... (B)選項文字 ... (C)選項文字 ... (D)選項文字 ...
    """
    # 使用正則表達式分組擷取各部分
    pattern = r"(\d+)\.\s*\(([A-D])\)\s*(.*?)\s*\(A\)(.*?)\s*\(B\)(.*?)\s*\(C\)(.*?)\s*\(D\)(.*)"
    match = re.match(pattern, text)
    if match:
        q_id, correct_answer, question, option_a, option_b, option_c, option_d = match.groups()
        return [
            q_id.strip(),
            question.strip(),
            option_a.strip(),
            option_b.strip(),
            option_c.strip(),
            option_d.strip(),
            correct_answer.strip()
        ]
    return None

def process_questions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["id", "question", "option_A", "option_B", "option_C", "option_D", "correct_answer"])
        
        buffer = ""  # 用來累積屬於同一題的所有行
        for line in infile:
            stripped_line = line.strip()
            # 若遇到以題號開頭的新行，代表可能開始了新題目
            if re.match(r'^\d+\.', stripped_line):
                # 如果 buffer 不空且符合完整題目的格式，則解析並寫入 CSV
                if buffer and is_complete_question(buffer):
                    parsed = parse_question(buffer)
                    if parsed:
                        csv_writer.writerow(parsed)
                # 開始新的題目，重新設定 buffer
                buffer = stripped_line
            else:
                # 否則，將該行加入目前的題目內容中
                buffer += " " + stripped_line
        
        # 檔案結尾時，處理剩餘的 buffer
        if buffer and is_complete_question(buffer):
            parsed = parse_question(buffer)
            if parsed:
                csv_writer.writerow(parsed)
    
    print(f"✅ 資料處理完成，已儲存至 {output_file}")

# 使用範例
process_questions("questions.txt", "questions.csv")
