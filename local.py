import json
import requests

print("\nВведите ваше имя:")
nameUser = input("---> ")
requests.post("http://127.0.0.1:3000/api/eventbets/users", {"name": nameUser, "points": 0})

while True:
    print("\nВыберите вариант:")
    print("1. Получить событие")
    print("2. Посмотреть ТОП событий")
    print("3. Посмотреть ТОП игроков")
    print("4. Создать событие")
    print("0. Выход")
    numberMenuMain = input("---> ")

    match numberMenuMain:
        case "1":
            event = json.loads(requests.get("http://127.0.0.1:3000/api/eventbets/events").json())
            while True:
                print("\n" + event["eventText"])
                print("1-й вариант: " + event["variant1"] + " ||| " + "2-й вариант: " + event["variant2"])

                print("\nВыберите вариант:")
                print("1. Сделать ставку")
                print("2. Оставить комментарий")
                print("3. Посмотреть комментарии")
                print("0. Вернуться")
                numberMenu1 = input("---> ")

                match numberMenu1:
                    case "1":
                        print("Введите ставку для 1-го варианта")
                        bet1 = input("---> ")
                        print("Введите ставку для 2-го варианта")
                        bet2 = input("---> ")
                        pointsTotal1 = int(bet1) * int(event["variantPoint1"])
                        pointsTotal2 = int(bet2) * int(event["variantPoint2"])
                        totalPointsUser = requests.put("http://127.0.0.1:3000/api/eventbets/users", {"name": nameUser,
                                                                                                     "points": pointsTotal1 + pointsTotal2}).text
                        requests.put("http://127.0.0.1:3000/api/eventbets/events", {"eventText": event["eventText"]})
                        print("Итого очков за 1-й вариант: " + str(pointsTotal1))
                        print("Итого очков за 2-й вариант: " + str(pointsTotal2))
                        print("Итого ваших очков: " + totalPointsUser)
                        break
                    case "2":
                        print("Введите комментарий: ")
                        myComment = input("---> ")
                        requests.post("http://127.0.0.1:3000/api/eventbets/comments", {"event": event["eventText"], "name": nameUser, "text": myComment})
                    case "3":
                        commentsList = json.loads(requests.get("http://127.0.0.1:3000/api/eventbets/comments", {"event": event["eventText"]}).json())
                        i = 1
                        for commentOne in commentsList:
                            print("\nИмя: " + commentOne["name"])
                            print("Комментарий: " + commentOne["text"])
                            i += 1
                        input("\nВведите любое значение, чтобы вернуться")
                    case "0":
                        break
                    case _:
                        print("Попробуйте снова")
                        continue
        case "2":
            eventsTop = json.loads(requests.get("http://127.0.0.1:3000/api/eventbets/events/top").json())
            i = 1
            for eventTop in eventsTop:
                print("\n" + str(i) + " место")
                print("Собыите: " + eventTop["eventText"])
                print("Количество ставок: " + str(eventTop["countBets"]))
                i += 1
            input("\nНажмите Enter, чтобы вернуться")
        case "3":
            usersTop = json.loads(requests.get("http://127.0.0.1:3000/api/eventbets/users/top").json())
            i = 1
            for userTop in usersTop:
                print("\n" + str(i) + " место")
                print("Имя: " + userTop["name"])
                print("Количество очков: " + str(userTop["points"]))
                i += 1
            input("\nНажмите Enter, чтобы вернуться")
        case "4":
            print("Введите событие")
            eventText = input("---> ")
            print("Введите Вариант 1")
            variant1 = input("---> ")
            print("Введите коэффициент за Вариант 1")
            variantPoint1 = input("---> ")
            print("Введите Вариант 2")
            variant2 = input("---> ")
            print("Введите коэффициент за Вариант 2")
            variantPoint2 = input("---> ")
            requests.post("http://127.0.0.1:3000/api/eventbets/events", {"eventText": eventText,
                                                                         "variant1": variant1,
                                                                         "variantPoint1": variantPoint1,
                                                                         "variant2": variant2,
                                                                         "variantPoint2": variantPoint2,
                                                                         "countBets": 0})

        case "0":
            break
        case _:
            print("Попробуйте снова")
            continue


# res = requests.post("http://127.0.0.1:3000/api/courses/3", {"name": "Golang", "videos": 5})
# print(res.json())