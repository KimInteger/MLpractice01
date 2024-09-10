from basic_data import basic_data

all_key_count = 0
traffic_count = 0
traffic_charge = 0
keyword = "교통"

def extract_keys_from_dict(data):
    global keyword, traffic_charge, traffic_count
    keys = []  # 키 값을 저장할 리스트
    if isinstance(data, dict):  # 데이터가 딕셔너리인 경우
        keys.extend(data.keys())  # 현재 딕셔너리의 키 값들을 추가
        for item in data.keys() :
            if keyword in item :
                traffic_count += 1
                if type(data[item]) == int :
                    traffic_charge += data[item]
        for value in data.values():
            if isinstance(value, dict):  # 만약 value가 또 다른 딕셔너리라면 재귀적으로 탐색
                keys.extend(extract_keys_from_dict(value))
    return keys

def extract_keys_from_list_of_dicts(data_list):
    global all_key_count
    all_keys = []  # 전체 키 값을 저장할 리스트
    for item in data_list:
        if isinstance(item, dict):  # 리스트 아이템이 딕셔너리라면 키 값을 추출
            all_keys.extend(extract_keys_from_dict(item))
            all_key_count = len(all_keys)
    return all_keys
                
                
result = extract_keys_from_list_of_dicts(basic_data)
print(result)
print(traffic_count)
print(traffic_charge)
print(all_key_count)