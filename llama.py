import requests
import json

API_URL = 'http://localhost:11434/api/generate'

def get_llama_response(question):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'llama3.1',
        'prompt': question,
        'stream': True
    }

    print(f"보내는 데이터: {data}")

    try:
        response = requests.post(API_URL, headers=headers, json=data, stream=True)
        response.raise_for_status()
        
        print(f"응답 상태 코드: {response.status_code}")
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                print(f"응답 데이터: {json_response}")
                if 'response' in json_response:
                    full_response += json_response['response']
                if json_response.get('done', False):
                    break
        
        return full_response.strip()
        
    except requests.exceptions.RequestException as e:
        return f"오류: API 요청 중 문제가 발생했습니다. {str(e)}"
    except json.JSONDecodeError:
        return "오류: 응답이 올바른 JSON 형식이 아닙니다."

def main():
    question = input("질문을 입력하세요: ")
    answer = get_llama_response(question)
    
    print(f"\n답변: {answer}")
    
    with open('qa_log.txt', 'a', encoding='utf-8') as file:
        file.write(f"질문: {question}\n")
        file.write(f"답변: {answer}\n")
        file.write('-' * 40 + '\n')

    print("질문과 답변이 파일에 저장되었습니다.")

if __name__ == "__main__":
    main()