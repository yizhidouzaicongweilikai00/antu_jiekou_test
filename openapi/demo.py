from flask import Flask
from flask_restful import Api, Resource, reqparse
from common.bytecontext import *
from component.api.launch_task_api import LaunchTaskAPI

app = Flask(__name__)
api = Api(app)


class Demo(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("marketingGoal", type=list)

    def get(self):
        data = self.parser.parse_args()
        context = ByteContext(data)
        LaunchTaskAPI().search_live_templates(context)
        return context.result


api.add_resource(Demo, '/getDemo', endpoint='demo')

if __name__ == '__main__':
    app.run(debug=True)
