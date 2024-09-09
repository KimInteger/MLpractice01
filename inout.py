my_family = input("성을 입력하세요 :")
my_name  = input("이름을 입력하세요 : ")


def print_name(family,name) :
    full_name = family + " "+ name
    print(f"나의 성은 {family}고, 나의 이름은 {name} 그래서 저의 이름은 {full_name}입니다.")
    
print_name(my_family,my_name)