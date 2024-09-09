import subprocess
import re
import os

# Llama 명령어 실행 함수
def run_llama(prompt):
    command = ["ollama", "run", "llama3.1", prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return f"Error: {result.stderr}"

# 질문을 파일 이름으로 변환
def sanitize_filename(prompt):
    # 파일 이름에 사용할 수 없는 문자들을 치환
    sanitized = re.sub(r'[\\/*?:"<>|]', '', prompt)
    # 공백을 밑줄로 변환
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized + ".md"

# 질문 파일을 저장할 디렉토리
SAVE_DIR = "/mnt/c/Users/Administrator/Desktop/output"

# 디렉토리가 없으면 생성
os.makedirs(SAVE_DIR, exist_ok=True)

# 질의응답을 반복하는 함수
def interactive_llama_session():
    print("질문을 입력하고 `exit`을 입력하면 종료됩니다.")
    
    while True:
        # 사용자로부터 질문 입력 받기
        question = input("나: ")

        # 'exit' 입력시 종료
        if question.lower() == "exit":
            print("종료합니다.")
            break

        # 파일 이름 생성
        file_name = sanitize_filename(question)
        file_path = os.path.join(SAVE_DIR, file_name)

        # Llama에게 질문 보내기
        answer = run_llama(question)

        # 응답을 파일에 기록
        with open(file_path, "w") as file:
            file.write(f"### 나: {question}\n")
            file.write(f"### Llama: {answer}\n")

        print(f"Llama의 응답이 {file_path}에 저장되었습니다.")

# 메인 함수 실행
if __name__ == "__main__":
    interactive_llama_session()
