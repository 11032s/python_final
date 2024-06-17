word = input( '請輸入開始:' )
import random

def generate_question():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    answer = num1 + num2
    return num1, num2, answer

def main():
    num1, num2, answer = generate_question()
    user_answer = input(f"請回答 {num1} + {num2} = ")
    
    try:
        user_answer = int(user_answer)
        if user_answer == answer:
            print("你好棒！")
        else:
            print("哈哈 繼續努力")
    except ValueError:
        print("請輸入有效的數字")

if __name__ == "__main__":
    main()
