import json

def json_to_python(file_path):
    """
    JSON 파일을 Python 객체로 변환하는 함수.
    
    Args:
    - file_path (str): JSON 파일의 경로
    
    Returns:
    - dict 또는 list: JSON 데이터를 파싱한 Python 객체
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            print("파일을 성공적으로 열었습니다.")  # 디버깅용 출력
            data = json.load(f)  # JSON 파일을 파싱하여 Python 객체로 변환
            print("JSON 데이터를 성공적으로 변환했습니다.")  # 디버깅용 출력
        return data
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 형식이 잘못되었습니다: {e}")
        return None
    except Exception as e:
        print(f"파일을 변환하는 중 오류가 발생했습니다: {e}")
        return None

data = json_to_python("notion_database_data.json")
print(data)  # 변환된 데이터를 출력
