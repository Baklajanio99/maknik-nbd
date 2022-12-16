import random
import pymongo
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from bson.json_util import dumps

# устанавливаем соединение с MongoDB
# MongoDB должна быть запущена на компьютере, 27017 - стандартный порт
db_client = pymongo.MongoClient("mongodb://localhost:27017/")

# подключаемся к БД eventbets, если её нет, то будет создана
current_db = db_client["eventbets"]

# получаем колекцию из нашей БД, если её нет, то будет создана
# Коллекция - это группа документов, которая хранится в БД MongoDB (эквалент таблицы в ркляционных базах)
events = current_db["events"]
users = current_db["users"]
comments = current_db["comments"]

app = Flask(__name__)
api = Api()

# Методы для событий
parserEvent = reqparse.RequestParser()
parserEvent.add_argument("eventText", type=str, location="form")
parserEvent.add_argument("variant1", type=str, location="form")
parserEvent.add_argument("variantPoint1", type=int, location="form")
parserEvent.add_argument("variant2", type=str, location="form")
parserEvent.add_argument("variantPoint2", type=int, location="form")
parserEvent.add_argument("countBets", type=int, location="form")

class Events(Resource):
    def get(self):
        randomNum = random.randint(1, events.count_documents({}))
        i = 1
        for event in events.find():
            if i == randomNum:
                return dumps(event)
            else:
                i += 1

    def post(self):
        events.insert_one(parserEvent.parse_args())

    def put(self):
        eventText = parserEvent.parse_args()["eventText"]
        events.update_one({"eventText": eventText},
                          {"$set": {"countBets": events.find_one({"eventText": eventText})["countBets"] + 1}})

# Методы для получения ТОПа собыйти
class EventsTop(Resource):
    def get(self):
        return dumps(events.find().sort("countBets", -1))

# Методы для users
parserUser = reqparse.RequestParser()
parserUser.add_argument("name", type=str, location="form")
parserUser.add_argument("points", type=int, location="form")

class Users(Resource):
    def post(self):
        if users.find_one({"name": parserUser.parse_args()["name"]}) is None:
            users.insert_one(parserUser.parse_args())

    def put(self):
        nameUser = parserUser.parse_args()["name"]
        users.update_one({"name": nameUser},
                         {"$set": {"points": users.find_one({"name": nameUser})["points"] + parserUser.parse_args()["points"]}})
        return users.find_one({"name": nameUser})["points"]

# Методы для usersTop
class UsersTop(Resource):
    def get(self):
        return dumps(users.find().sort("points", -1))

# Методы для комментариев
class Comments(Resource):
    def get(self):
        return dumps(comments.find({"event": request.args["event"]}))
        
    def post(self):
        parserComment = reqparse.RequestParser()
        parserComment.add_argument("event", type=str, location="form")
        parserComment.add_argument("name", type=str, location="form")
        parserComment.add_argument("text", type=str, location="form")
        comments.insert_one(parserComment.parse_args())

api.add_resource(Events, "/api/eventbets/events")
api.add_resource(EventsTop, "/api/eventbets/events/top")
api.add_resource(Users, "/api/eventbets/users")
api.add_resource(UsersTop, "/api/eventbets/users/top")
api.add_resource(Comments, "/api/eventbets/comments")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")