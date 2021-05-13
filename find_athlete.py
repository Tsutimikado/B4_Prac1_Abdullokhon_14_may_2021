import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import lets_connect
from users import request_data as ask
from users import User


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base=declarative_base()

lets_connect()

def date_convert(date): #переводит дату в формат подобный datastamp. 
    split_=date.split('.')
    newdate=int(split_[0])+int(split_[1])*31+int(split_[2])*372
    return newdate

    #31 december 2000, 1 january 2001, 25 december 2000 ? 

def near_brn(u_bd,all_bd): #Получает дату рождения и список всех дат, чтобы найти ближайшего. 
    dif=1100000
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


    query_all=session.query(User)
       
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
    query = session.query(User).filter(User.id == n_ih)
    name_height=[user.first_name for user in query.all()][0]
    print ("Рост участника #{id} {name_height} отличатеся от {name_u} всего на {dif} метра".format(id=n_ih, name_height=name_height, name_u=name, dif=n_hd))
    
    user_bds_list=[user.birthdate for user in query_all.all()]
    for a,b in zip(user_ids, user_bds_list):
        user_bds[a]=date_convert(b)
    del user_bds[int(in_id)]
    n_ib=near_brn(bd,user_bds)
    query = session.query(User).filter(User.id == n_ib)
    name_birth=[user.first_name for user in query.all()][0]
    print ("#{id} {b_name} и {u_name} почти ровестники!".format(id=n_ib, b_name=name_birth,u_name=name) )

if __name__=='__main__':
    main()