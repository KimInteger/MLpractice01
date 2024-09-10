from basic_data import basic_data

def extract_keys_from_dict(data):
    keys = []  # 키 값을 저장할 리스트
    if isinstance(data, dict):  # 데이터가 딕셔너리인 경우
        keys.extend(data.keys())  # 현재 딕셔너리의 키 값들을 추가
        for value in data.values():
            if isinstance(value, dict):  # 만약 value가 또 다른 딕셔너리라면 재귀적으로 탐색
                keys.extend(extract_keys_from_dict(value))
    return keys

def extract_keys_from_list_of_dicts(data_list):
    all_keys = []  # 전체 키 값을 저장할 리스트
    for item in data_list:
        if isinstance(item, dict):  # 리스트 아이템이 딕셔너리라면 키 값을 추출
            all_keys.extend(extract_keys_from_dict(item))
    return all_keys
                
                
result = extract_keys_from_list_of_dicts(basic_data)
print(result)