def read(num):
    result = []
    for j in range(1, 10):  # 控制乘數的範圍
        result.append(f"{num} x {j} = {num * j}")  # 構建每一個乘法表運算式及結果
    return result

if __name__ == '__main__':
    while True:
        try:
            num = int(input("請輸入要查詢的數字 (1-9): "))
            if 1 <= num <= 9:
                tables = multiplication_table(num)
                for table in tables:
                    print(table)  # 輸出該數字的九九乘法表
                break  # 成功輸出後退出循環
            else:
                print("請輸入有效的數字 (1-9)。")
        except ValueError:
            print("請輸入有效的數字。")
