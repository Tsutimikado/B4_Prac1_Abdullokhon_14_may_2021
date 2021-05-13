from users import main as log_user
from find_athlete import main as find_user

print("Добро пожаловать в мою программу.")
def main():	
	mode=input("""\nВыберите режим в котором хотите работать далее:
		1 - Использовать users.py
		2 - Использовать find_athlete
		3 - Выйти из программы 
		""")

	if mode== "1":
		log_user()
		main()
	elif mode=="2":
		find_user()
		main()
	elif mode == "3":
		exit()
	else:
		print("Ошибка ввода")
		main()

if __name__=="__main__":
	main()
