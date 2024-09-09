my_name  = input("이름을 입력하세요 : ")


def print_name(name) :
    if(name) :
        family = name[0]
        own_name = name[1:]
    full_name = family + own_name
    print(f"나의 성은 '{family}'이고, 나의 이름은 '{own_name}'입니다. 그래서 저의 이름은 {full_name}입니다.")
    
print_name(my_name)