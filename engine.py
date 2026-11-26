# # # def main() :
# # #     #while True:
# # #         x = input ("Choose one of this options 1, 2 or 3")
# # #         match x: 
# # #             case '1':
# # #                 for i in range(5):
# # #                     print ("WIN!!!", i)
# # #             case '2':
# # #                 print ("LOST")
# # #             case '3':
# # #                 print ("LOST")    
# # #             case 'STOP':
# # #                 exit
# # # main()
# # # print("ლუწებია")
# # # for i in range(2, 10, 2):
# # #     print(i, end= "." "\n")
# # # print("კენტებია")
# # # for i in range(1, 10, 2):
# # #     print(i, end= "." "\n")

# # # for i in range(1, 11):
# # #     print(i)
# # # for i in range(100, 1, -2):
# # #     print(i)

# # # for i in range(1, 12, 2):
# # #     print(i * 0)
# # # ხილი = ["ვაშლი", "ბანანი", "ფორთოხალი"]
# # # for x in ხილი:
# # #     print("მე მიყვარს:", x)

# # # x = ["Luka", "Giorgi", "Nika"]
# # # for x in enumerate(x):
# # #     print("number is:", x)

# # # y = {"Luka": 2, "banana": 3}
# # # for product, x in y.items():
# # #     print(product, "cost", x, "GEL")

# # # names = ["Luka", "Anastasiia"]
# # # points = [95, 100]
# # # for names, x in zip(names, points):
# # #     print(names, "got", x)

# # # nome = ["Luka", "Anastasiia"]
# # # cognome = ["Tcheishvili", "Chernova"]
# # # for nome, x in zip(names, cognome):
# # #     print(nome, "", x, sep="") 
# # # password = ""
# # #  # while password != "secret1234":
# # #      password != input("your password")
# # #      print("right, welcome back")
# # #     elif()
# # #      print("wrong, try again")
 
# # # x = int(input("your point:"))
# # # if x > (int(51)):
# # #     print("you have passed! you have", x, "point. Congratulations", sep=" ")
# # # elif x > (int(99)):
# # #     print("you got a", x, "that is maximum point! congratulations", sep=" ")
# # # else:
# # #     print("I am so sorry, you got", x, "points, unfortunatelly you have failed", sep=" ")

# # # def point():
# # #     x = bool(input("What is your mark? "))
# # #     if x == 100:
# # #         print ("Exelent! you have maximum", "100", "point!", sep=" ")
# # #     elif x >= 49.6:
# # #         print ("Congratulations, you have passed the exam! ")
# # #     elif x < 49.6:
# # #         print("I am sorry, you have failed the exam, minimum points to pass is 50")

# # # point()


# # # def simple_calculator(a, b, op):
# # #         match op:
# # #             case '+':
# # #                 return a + b
# # #             case '-':
# # #                 return a - b
# # #             case '*':
# # #                 return a * b
# # #             case '/':
# # #                 if b == 0:
# # #                     return "error: division by zero"
# # #                 else:
# # #                      return a / b 
    

    
# # # a = int(input("a: "))
# # # b = int(input("b: "))
# # # op = input("op: ")
# # # # if (int(b)) == '0' and op == '/':
# # # #     print("Error: division by zero ")     

# # # print (simple_calculator(a, b, op))



# # # def calculator(x, y, o):
# # #     match o:
# # #         case "+":
# # #             return x + y
# # #         case "-":
# # #             return x - y
# # #         case "*":
# # #             return x * y
# # #         case "_":
# # #             return "invalid operation"
    
# # # x = float(input("first number: "))
# # # y = float(input("secpnd number: "))
# # # o = (input("choose operation: "))
# # # print (calculator)



# # # def cal(A, B, OP):
# # #     match OP:
# # #         case "+":
# # #             return A + B
# # #         case "-":
# # #             return A - B
# # #         case "*":
# # #             return A * B
# # #         case "/":
# # #             if B == 0:
# # #                 return "error: division by zero"
# # #             return A / B
         
# # # A = int(input("A: "))
# # # B = int(input("B: "))
# # # OP = input("OP: ")
# # # print (cal(A, B , OP))        

# # # s = 0
# # # i = 1
# # # while i <= 10:
# # #     if i % 2 == 0:
# # #         s += i
# # #     i += 1
# # # print (s)    
# # # i = 1
# # # s = 0
# # # # N = int(input("positive number: "))
# # # while i <= N:
# # #     if i % 2 != 0:
# # #         s += i
# # #     i += 1
# # # print(s)

# # # i = 1
# # # s = 0
# # # N = int(input("your number: "))
# # # while i + 1 <= N:
# # #     i *= i + 1
# # # s += i
# # # print(s)    

# # # i = 1
# # # product = 1  # ნამრავლის საწყისი მნიშვნელობა
# # # N = int(input("your number: "))

# # # while i <= N:
# # #     product *= i  # იგივეა, რაც product = product * i
# # #     i += 1        # i უბრალოდ იზრდება 1-ით (1, 2, 3, 4...)

# # # print(product)

# # # N = int(input("number: "))
# # # while N >= 1:
# # #     print (N)
# # #     N -= 1
# # # print ("Go! ")    

# # # n = int(input("number: "))
# # # for i in range (n, 0, -1):
# # #     print (i)
# # # print("Go! ")    

# # # g = int(input("number: "))
# # # if g % 2 != 0:
# # #     g -= 1
# # # for i in range (g, 0, -2):
# # #     print (i)
# # # print ("Done! ")

# # # def count_digit(n, d):
# # #     count = 0
# # #     for digit in str(n):
# # #         if digit == str(d):
# # #             count += 1
# # #     return count
# # # print(count_digit(1213141, 1))


# # # def count(n, d):
# # #     count = 0
# # #     for digit in str(n):
# # #         if digit == str(d):
# # #             count += 1
# # #     return count
# # # print(count(1111110, 0))       

# # # def counts(a, b):
# # #     count = 0
# # #     for digit in str(a):
# # #         if digit == str(b):
# # #             count += 1
# # #     return count
# # # print (counts(13245555, 5)) 

# # # def C(a, b):
# # #     count = 0
# # #     for digit in str(a):
# # #         if digit == str(b):
# # #             count += 1
# # #     return count
# # # print (C(1111111, 1))   





# # # def X(a, b):
# # #     count = 0
# # #     for digit in str(a):
# # #         if digit == str(b):
# # #          count += 1
# # #     return count
# # # print (X(44444, 4))





# # # def G(f, l):
# # #     count = 0
# # #     for digit in str(f):
# # #         if digit == str(l):
# # #             count += 1
# # #     return count
# # # print(G(100000, 0))     



# # # def L(a, b):
# # #     count = 0
# # #     for digit in str(a):
# # #         if digit == str(b):
# # #             count += 1
# # #     return count
# # # print (L(2222222, 2))   




# # # def count_evens(n):
# # #     count = 0
# # #     for digit in str(n):
# # #         if str(digit) % 2 == 0:
# # #             count += 1
# # #     return count
# # # print (count_evens(8124213))        

# # # def h(n):
# # #     if n <= 1:
# # #         return n
# # #     return h(n - 1) + h(n - 2)


# # # def sum_recursive(n):
# # #     if n == 1:
# # #         return 1
# # #     return n + sum_recursive(n - 1)

# # # # აუცილებელია print()-ით გამოძახება, რომ ეკრანზე გამოჩნდეს!
# # # print(sum_recursive(5))

# # # def remove_duplicates(lst):
# # #     unique_lst = []
    
# # #     for item in lst:
# # #         # თუ ელემენტი ჯერ არ არის ახალ სიაში, ვამატებთ
# # #         if item not in unique_lst:
# # #             unique_lst.append(item)
            
# # #     return unique_lst

# # # # შემოწმება:
# # # numbers = [1, 2, 2, 3, 1, 4]
# # # print(remove_duplicates(numbers))  # დაიბეჭდება: [1, 2, 3, 4]





# # # def remove_dublicate(list):
# # #     unique_lst = []
# # #     for item in list:
# # #         if item not in unique_lst:
# # #             unique_lst.append(item)
# # #     return unique_lst
# # # numbers = [4, 4, 4, 4, 5, 2, 14, 457, 62,]
# # # print(remove_dublicate(numbers))        

# # # def add_binary(a, b):
# # #     result = []
# # #     carry = 0
    
# # #     # ინდექსები ბოლო სიმბოლოებიდან იწყება
# # #     i = len(a) - 1
# # #     j = len(b) - 1
    
# # #     # სანამ რომელიმე სტრიქონში დარჩა ციფრები ან carry > 0
# # #     while i >= 0 or j >= 0 or carry:
# # #         total = carry
        
# # #         # თუ a-ში ჯერ კიდევ არის ციფრი
# # #         if i >= 0:
# # #             total += int(a[i])
# # #             i -= 1
            
# # #         # თუ b-ში ჯერ კიდევ არის ციფრი
# # #         if j >= 0:
# # #             total += int(b[j])
# # #             j -= 1
            
# # #         # მიმდინარე ციფრი არის total % 2
# # #         result.append(str(total % 2))
        
# # #         # გადასატანი ნაშთი/მახსოვრობა (0 ან 1)
# # #         carry = total // 2
        
# # #     # რადგან ბოლოდან ავაწყვეთ, გადავაბრუნოთ და შევაერთოთ ტექსტად
# # #     return "".join(result[::-1])

# # # # შემოწმება:
# # # print(add_binary("1011", "111"))  # დაიბეჭდება: "10010"


# # # list = []
# # # list.append(6)
# # # print(list)

# # # x = input("who are you? ")
# # # print (x)[::-1]
# # # backward = input("write something and i will reverse it: ")
# # # print(backward[::-1])


# # # vowels = [ "a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
# # # not_vowels = [ "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
# # # x = input("word: ")
# # # NW = 0
# # # count = 0 
# # # for letter in x:
# # #     if letter in vowels:
# # #         count += 1

# # # for letter in x:
# # #     if letter in not_vowels:
# # #         NW += 1
# # # print("თანხმოვნების რაოდენობა: ", NW)    
# # # print("ხმოვნების რაოდენობა: ", count)

# # # Y = int(input("number: "))
# # # # match Y % 2:
# # # #     case 0:
# # # #         print("number is even: ")
# # # #     case 1:
# # # #         print("number is odd: ")

# # # # if Y % 2 ==0:
# # # #     print("number is even. ")
# # # # if Y % 2 != 0:
# # # #     print("number is odd. ")            
        
# # # match Y:
# # #     case Y if Y % 2 == 0:
# # #         print("number is even. ")
# # #     case Y if Y % 2 != 0:
# # #         print("number is odd. ")    

# # def convert(a, b):
# #     # თუ რიცხვი 0-ია
# #     if a == 0:
# #         return "0"
    
# #     # 10-იდან 15-ის ჩათვლით ნაშთების შესაბამისი სიმბოლოები
# #     digits = "0123456789ABCDEF"
# #     result = ""
    
# #     # ვინახავთ რიცხვის ნიშანს (თუ უარყოფითია)
# #     is_negative = a < 0
# #     a = abs(a)
    
# #     # ციკლი უწყვეტი გაყოფისთვის
# #     while a > 0:
# #         remainder = a % b         # ვიღებთ ნაშთს
# #         result = digits[remainder] + result  # ნაშთს ვამატებთ შედეგის დასაწყისში
# #         a = a // b                # ვიღებთ მთელ ნაწილს
        
# #     return "-" + result if is_negative else result


# # # შემოწმება მაგალითების მიხედვით:
# # user_number = int(input("შეიყვანეთ რიცხვი: "))
# # base = int(input("შეიყვანეთ ფუძე (2-იდან 16-მდე): "))

# # if 2 <= base <= 16:
# #     print(f"შედეგი: {convert(user_number, base)}")
# # else:
# #     print("ფუძე უნდა იყოს 2-იდან 16-ის ჩათვლით!")

# # def get_level_xp(level, base=20, growth=1.20):
# #   # ითვლის კონკრეტული ლეველის ასაღებად საჭირო ქულებს მთელ რიცხვამდე დამრგვალებით
# #   return round(base * (growth**level))


# # # მაგალითად, პირველი 10 ლეველის ნახვა:
# # total_xp = 0
# # for lvl in range(0, 11):
# #   req_xp = get_level_xp(lvl)
# #   total_xp += req_xp
# #   print(f"ლეველი {lvl}: საჭიროა {req_xp} XP (სულ ჯამში: {total_xp} XP)")
# # def calculate_level_requirements(max_level=100, base_xp=20, growth_rate=0.10):
# #   """ითვლის თითოეული ლეველის ასაღებად საჭირო და ჯამურ XP-ს ლიმიტის გარეშე."""
# #   total_xp = 0
# #   print(f"{'ლეველი':<100} | {'საჭირო XP':<15} | {'ჯამური XP':<15}")
# #   print("-" * 46)

# #   for level in range(max_level + 1):
# #     # ფორმულა: საწყისი * (1 + ზრდა)^ლეველი
# #     required_xp = round(base_xp * ((1 + growth_rate) ** level))
# #     total_xp += required_xp
# #     print(f"{level:<100} | {required_xp:<15,} | {total_xp:<15,}")


# # # ტესტირება პირველ 25 ლეველზე
# # calculate_level_requirements(100)

# from dataclasses import dataclass, field
# from typing import Dict, List


# ACTIVITY_MULTIPLIERS: Dict[str, int] = {
#     "სამუშაო": 5,
#     "აკადემიური მიღწევა": 3,
#     "ფიზიკური": 4,
#     "პერსონალური განვითარება და დახელოვნება": 7,
#     "ურთიერთობები": 4,
#     "ჰობი და თავისუფალი დრო": 6,
#     "თავგადასავლები": 8,
# }

# DAILY_TASKS_EXP: Dict[str, int] = {
#     "ძილი": 30,
#     "ჭამა 1": 20,
#     "ჭამა 2": 25,
#     "მეცადინეობა": 50,
#     "სუფთა ჰაერზე ყოფნა": 15,
#     "კბილების ორჯერ გამოხეხვა": 10,
# }


# def exp_needed_for_level(level: int, base_exp: int = 20, growth_rate: float = 0.10) -> int:
#     """აბრუნებს კონკრეტული ლეველის (level >= 1) მისაღწევად საჭირო დამრგვალებულ EXP-ს."""
#     if level < 1:
#         return 0
#     return round(base_exp * ((1.0 + growth_rate) ** (level - 1)))


# def total_exp_for_level(level: int, base_exp: int = 20, growth_rate: float = 0.10) -> int:
#     """აბრუნებს ჯამურ EXP-ს, რომელიც საჭიროა 0-დან მოცემულ ლეველამდე ასასვლელად."""
#     return sum(exp_needed_for_level(lvl, base_exp, growth_rate) for lvl in range(1, level + 1))


# @dataclass
# class PlayerProgress:
#     exp: int = 0
#     level: int = 0
#     category_exp: Dict[str, int] = field(default_factory=lambda: {
#         "ყოველდღიური დავალებები": 0,
#         **{cat: 0 for cat in ACTIVITY_MULTIPLIERS},
#         "მიზნები": 0,
#     })
#     history: List[str] = field(default_factory=list)

#     def _recalculate_level_up_only(self) -> None:
#         """ლეველი იზრდება მხოლოდ მაშინ, როცა ჯამური EXP აღწევს შემდეგი ლეველის ზღვარს."""
#         while total_exp_for_level(self.level + 1) <= self.exp:
#             self.level += 1

#     def _apply_exp(self, delta: int, source_category: str, description: str) -> int:
#         self.exp += delta
#         self.category_exp[source_category] = self.category_exp.get(source_category, 0) + delta
#         self._recalculate_level_up_only()
#         self.history.append(f"{description} | EXP: {delta:+d} | ჯამური EXP: {self.exp} | ლეველი: {self.level}")
#         return delta

#     def log_daily_task(self, task_name: str, completed: bool) -> int:
#         if task_name not in DAILY_TASKS_EXP:
#             raise ValueError(f"უცნობი ყოველდღიური დავალება: {task_name}")
#         base = DAILY_TASKS_EXP[task_name]
#         delta = base if completed else -base
#         status = "შესრულდა" if completed else "არ შესრულდა"
#         return self._apply_exp(delta, "ყოველდღიური დავალებები", f"[ყოველდღიური] {task_name} ({status})")

#     def log_activity(self, category: str, completed: bool) -> int:
#         if category not in ACTIVITY_MULTIPLIERS:
#             raise ValueError(f"უცნობი აქტივობის კატეგორია: {category}")
#         raw_points = 5 if completed else -5
#         delta = raw_points * ACTIVITY_MULTIPLIERS[category]
#         status = "შესრულდა" if completed else "არ დასრულდა"
#         return self._apply_exp(delta, category, f"[აქტივობა] {category} ({status}, ×{ACTIVITY_MULTIPLIERS[category]})")

#     def log_goal(self, goal_name: str, multiplier: int, completed: bool) -> int:
#         if multiplier <= 0:
#             raise ValueError("მიზნის კოეფიციენტი უნდა იყოს 0-ზე მეტი მთელი რიცხვი.")
#         raw_points = 5 if completed else -5
#         delta = raw_points * multiplier
#         status = "შესრულდა" if completed else "ჩავარდა"
#         return self._apply_exp(delta, "მიზნები", f"[მიზანი] {goal_name} ({status}, ×{multiplier})")