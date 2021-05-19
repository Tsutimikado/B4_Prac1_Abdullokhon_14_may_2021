import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base=declarative_base()

class User(Base):
    __tablename__='user'
    id=sa.Column(sa.Integer(), primary_key=True)
    first_name=sa.Column(sa.Text())
    last_name=sa.Column(sa.Text())
    gender=sa.Column(sa.Text())
    email=sa.Column(sa.Text())
    birthdate=sa.Column(sa.Text())
    height=sa.Column(sa.Float())

def lets_connect():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session=sessionmaker(engine)
    return session()

def select_gender(): #Реализовывает выбор пола участника из 2х имеющихся вариантов
    check_gender= input("""
Выберите свой пол:
1 - Я женщина
2 - Я мужчина
        """
        #3 - Я вертолёт
        )

    if check_gender == "1":
        return "female"
    elif check_gender == "2":
        return "male"
    else:
        print("Выберите пожалуйста из имеющихся вариантов.")
        select_gender()

def valid_email(email):
  """
  Проверяет наличие хотя бы одной точки в домене и одного знака @ в email. Возвращает True, если email допустимый, и False — в противном случае.
  """
  test=email.split("@")
  if len(test)!=2:
    return False
  else:
    if "." in test[1]:
        return True
    else:
        return False
# def get_id():
#  Должен был генерировать Id, но потом я заметил автозаполнение этого поля заданого заранее. Спасибо за облегчение работы.
#     last_id=session.query(User).count()
#     return last_id+1

def date_in(): # упрощает ввод даты рождения для минимализации ошибок и убирает надобность в функции проверки праильности введённых данных
    yy=input("В каком году Вы родились? \n")
    mm=input("Какой по счёту месяц это был? \n")
    dd= input("И наконец, в какой день этого месяца Вы родились?\n")
    return "%s.%s.%s"%(yy,mm,dd)


def request_data():
    print("Здравствуйте. Позвольте записать Ваши данные")
    first_name=input("Как Вас зовут?\n")
    last_name=input("Назовите свою фамилию, пожалуйста\n")
    gender= select_gender()
    email= input("Позвольте записать адресс вашей почты\n")
    while not valid_email(email):
        email= input("Адресс указан неверно. Давайте перезапишем его:\n")
    birthdate=date_in()
    height=input("Какой у Вас рост в метрах?\n")

    user=User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
        )
    return user
def main():
    session=lets_connect()
    user=request_data()
    session.add(user)
    session.commit() 
    print("Благодарю. Я записал Ваши данные")

if __name__ == "__main__":
    main()
