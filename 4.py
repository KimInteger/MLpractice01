import numpy as np

my_travel_charge = {
    "기차표 왕복": 80000,
    "카츠멘숀 삿포로라멘 미니안심세트": 14500,
    "소곱창고기국": 10000,
    "합천국밥": 10000,
    "버거킹 롱치킨 버거 세트": 5500,
    "숙박비스테이미도": 55000,
    "굿즈": 300000,
    "피시방": 5000,
    "노래방": 8000,
    "오락실 태고의 달인": 3000,
    "오락실 유비트": 3000,
    "오락실 노스텔지어": 3000,
    "오락실 팝픈뮤직": 1000,
    "교통비": 30000,
    "지스타 입장표값 BTC": 15000,
}

# 딕셔너리의 값을 NumPy 배열로 변환
charges_array = np.array(list(my_travel_charge.values()))

# 총비용 계산
total_charge = np.sum(charges_array)

print(f"총 여행 비용은 {total_charge}원입니다.")