from inspect_type import convert_question

question_answer = input("뭘 하시겠어요? :")

def run_what(answer) :
    if(answer == '노드') :
        print('node')        
        return
    elif(answer == '타입') :
        convert_question(input("아무말 렛츠게잇 : "))
        return
    
run_what(question_answer)