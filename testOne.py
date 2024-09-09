a = "인티저"
b = "김인트"

def string_merge() :
    global a, b
    return a + b

print(string_merge())

# * 맨날 이름쓰기 힘듦
def example() :
    return "예제"

anther_example = lambda: "예제"

add = lambda x,y : x+y
print(add(3,56))


array = ["배성빈", "문혜림", "신지윤"]


# key 부분도 ""을 사용함. 
obj = {
    "조자연" : "네이처 조",
    "김보미" : "개굴",
    "황재민" : "러스트",
    "황재민" : "수면왕"
}

print(obj["황재민"])


# 튜플이라고 함. 중복을 허용하지 않는다.
# 불변이다. 상수수준의 레벨을 가지고 있다.
another_obj = ("김인티저","송이현","유진초이", "유진초이")

print(another_obj)