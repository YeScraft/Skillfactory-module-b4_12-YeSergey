import datetime
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key = True)
    name = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key = True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    return Session()

def find_user(user_id, session):
    user = session.query(User).filter(User.id==user_id).first()
    if user:
        user_height = user.height
        user_bds = user.birthdate.split("-")
        user_name = user.first_name
        user_last = user.last_name
        user_bd = []
        for number in user_bds:
            float_n = int(number)
            user_bd.append(float_n)
        return user_height, user_bd, user_name, user_last, user_id
    else:
        user_height=user_bd=user_name=user_last=user_id = None
        return user_height, user_bd, user_name, user_last, user_id

def find_athelete(user_height, user_bd, session):
    athelets = session.query(Athelete).all()
    a_h = [athelete.height for athelete in athelets]
    d_a_h = []
    for number in filter(lambda number:number is not None, a_h):
        d_a_h.append(number) # отбраковывает атлетов у которых не указан рост
    closer_a_h = min(d_a_h, key=lambda x:abs(x-user_height)) # находит максимально близкое значение роста в эталону
    a_b = [[athelete.birthdate.split("-"), athelete.id] for athelete in athelets] # создаёт список из дат рождений и id
    for item in a_b:
        for i, number in enumerate(item[0]):
            item[0][i] = int(number)
    user_d = datetime(user_bd[0], user_bd[1], user_bd[2])
    a_d = []
    distans = 10000
    for item in a_b: # методом вычитания дат библиотеки datetime находим id с минимальной разницой в днях
        athelete_d = datetime(item[0][0], item[0][1], item[0][2])
        d = abs((user_d - athelete_d).days) # разница в днях
        if d==0 or d<=d and d<distans:
            distans = d
            a_id = item[1]
    # В задании требуется "...  вывести на экран двух атлетов: ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю"
    athelete_h = session.query(Athelete).filter(Athelete.height==closer_a_h).first()
    athelete_b = session.query(Athelete).filter(Athelete.id==a_id).first()
    return athelete_h, athelete_b

def answer_print(athelete_h, athelete_b, user_height, user_bd, user_name, user_last, user_id):
    print("\nДля пользователя с id: {} ({} {}: дата рождения: {}, рост: {} см) наидены следующие совпадения:".format(user_id, user_name, user_last, user_bd, user_height))
    print("По росту атлет: id: {}, имя: {}, рост: {}.".format(athelete_h.id, athelete_h.name, athelete_h.height))
    print("По дате рождения атлет: id: {}, имя: {}, дата рождения: {}.\n".format(athelete_b.id, athelete_b.name, athelete_b.birthdate))

def main():
    mode = 0
    while mode != "2":
        session = connect_db()
        mode = input("""Выбери режим:
        1 - Найти ближайшего к пользователю атлета;
        2 - Закончить поиск.\n""")
        if mode == "1":
            user_id = int(input("\nВведи id пользователя для поиска (целочисленное значение): "))
            user_height, user_bd, user_name, user_last, user_id = find_user(user_id, session)
            if user_id == None:
                print("\nНет такого id.\n")
            else:
                athelete_h, athelete_b = find_athelete(user_height, user_bd, session)
                answer_print(athelete_h, athelete_b, user_height, user_bd, user_name, user_last, user_id)
        elif mode == "2":
            print("Благодарю за сотрудничество!")
            StopIteration
        else:
            print("\nНекорректный режим!\n")

if __name__ == "__main__":
    main()