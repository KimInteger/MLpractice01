def convert_question(question_answer) :
    if(question_answer.isdecimal()) : 
        insepct_type(int(question_answer))
        return
    insepct_type(question_answer)


def insepct_type (answer) :
    if(answer) :
        answer_type = type(answer)
        print(f"적으신 것의 타입은 {answer_type}입니다.")
        