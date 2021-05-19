import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import lets_connect
from users import request_data as ask
from users import User
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base=declarative_base()

class Athelete(Base):

    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def date_convert(date): #переводит дату(text) в формат datetime.date 
    if "-" in date:
        split_=date.split('-')
    else:
        split_=date.split('.') #Да, я мог поменять тип ввода в своей программе и не создавать новые условия, но мне хочется оставить всё так.
    newdate=datetime.date(*map(int,split_))
    return newdate

    #1 march 2000 28 february 26 february

def near_brn(u_bd,all_bd): #Получает дату рождения и список всех дат, чтобы найти ближайшего. 
    dif=abs(u_bd-datetime.date(2077, 12, 10)) #Атсылоччччка
    did=None
    for iid,iter_  in all_bd.items():
        if abs(u_bd-iter_)<dif:
            dif=abs(u_bd-iter_)
            did=iid
    return did

def near_height(u_h, all_h):
    dif=1100000
    did=None
    for iid,iter_  in all_h.items():
        if iter_ is not None:
            if abs(float(u_h)-float(iter_))<dif:
                dif=abs(float(u_h)-float(iter_))
                did=iid
    return did, round(dif,2)

def find_user(session):
    id_=input("Позвольте узнать идентификатор искомого участника \n")
    query = session.query(User).filter(User.id == id_)
    if query.count() == 0:
        # print('Участникик с этим идентификатором не найден. Перепроверьте данные и попробуйте ещё раз')
        return False, None, None,None,None
    else:
        name = [user.first_name for user in query.all()][0]
        bd = date_convert([user.birthdate for user in query.all()][0])
        height = [user.height for user in query.all()][0]
        print("Ваш выбор пал на {}".format(name))
        return True, name, id_, height,bd

def main():
    session=lets_connect()
    find_true,name,in_id,height,bd=find_user(session)
    while not find_true:
        print('Участникик с этим идентификатором не найден. Перепроверьте данные и попробуйте ещё раз')
        find_true,name, in_id,height,bd =find_user(session)


    query_all=session.query(Athelete)
       
    user_heights={}
    user_bds={}
    # users_cnt = query.count()
    # print(users_cnt)
    user_ids=[user.id for user in query_all.all()]

    user_heights_list=[user.height for user in query_all.all()]
    for a,b in zip(user_ids, user_heights_list):
        user_heights[a]=b
    del user_heights[int(in_id)]
    n_ih,n_hd = near_height(height, user_heights)
    query = session.query(Athelete).filter(Athelete.id == n_ih)
    name_height=[user.name for user in query.all()][0]
    print ("Рост участника #{id} {name_height} отличатеся от {name_u} всего на {dif} метра".format(id=n_ih, name_height=name_height, name_u=name, dif=n_hd))
    
    user_bds_list=[user.birthdate for user in query_all.all()]
    for a,b in zip(user_ids, user_bds_list):
        user_bds[a]=date_convert(b)
    del user_bds[int(in_id)]
    n_ib=near_brn(bd,user_bds)
    query = session.query(Athelete).filter(Athelete.id == n_ib)
    name_birth=[user.name for user in query.all()][0]
    print ("#{id} {b_name} и {u_name} почти ровестники!".format(id=n_ib, b_name=name_birth,u_name=name) )

if __name__=='__main__':
    main()
