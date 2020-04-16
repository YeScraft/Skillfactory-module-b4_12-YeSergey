import sqlalchemy as sa
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# константа, указывающая способ соединения  с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key = True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)

def connect_db():
    engine = sa.create_engine(DB_PATH, echo = False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    return Session()

def request_data(session):
    print("Введите данные пользователя!")
    first_name = input("Введите имя: ").capitalize()
    last_name = input("Введите фамилию: ").capitalize()
    gender = input("Введите пол (male/female): ").lower()
    email = input("Введите адрес электронной почты: ").lower()
    birthdate = input("Введите дату рождения (ГГГГ-ММ-ДД): ")
    height = input("Введите рост в метрах (сантиметры отделять точкой): ")
    # users = [User for User in session.query(User)]
    # if users:
    #     max_id = 1
    #     for user in users:
    #         if user.id >= max_id:
    #             max_id = user.id
    #         else: print("Этого не может быть!")
    #     user_id = max_id + 1
    # else:
    #     user_id = 1
    user = User(
        #id = user_id,
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
        )
    return user

def find(name, session):
    user_q = session.query(User).filter(User.first_name == name)
    user_list = []
    for user in user_q.all():
        user_dict = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "id": user.id,
            "gender": user.gender,
            "birthdate": user.birthdate,
            "height": user.height,
            }
        user_list.append(user_dict)
    return user_list

def users_print(user_list, name):
    if user_list:
        for user in user_list:
                print("\nНайдено:\nname: {} {}, id: {}, gender: {}, birthdate: {}, height: {} \n".format(user["first_name"],
                                                                                                            user["last_name"],
                                                                                                            user["id"],
                                                                                                            user["gender"],
                                                                                                            user["birthdate"],
                                                                                                            user["height"]))
    else: print("\nПользователь %s не найден.\n"%name)

def main():
    mode = 0
    while mode != "3":
        session = connect_db()
        mode = input("""Выбери режим:
        1 - Зарегистрировать нового пользователя;
        2 - Найти зарегистрированного пользователя;
        3 - Закончить регистрацию.\n""")
        if mode == "1":
            user = request_data(session)
            session.add(user)
            session.commit()
            print("\nПользователь %s зарегистрирован\n"%user.first_name)
        elif mode == "2":
            name = input("\nВведи имя пользователя с заглавной буквы: ")
            user_list = find(name, session)
            users_print(user_list, name)
        elif mode == "3":
            print("\nБлагодарю за сотрудничество!")
            StopIteration
        else:
            print("\nНекорректный режим!\n")

if __name__ == "__main__":
    main()
