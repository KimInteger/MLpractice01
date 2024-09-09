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
    "황재민" : "러스트"
}

print(obj["조자연"])