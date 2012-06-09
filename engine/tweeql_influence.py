__author__ = 'kristof.leroux@gmail.com'

import general_settings
from tweeql.exceptions import TweeQLException
from tweeql.field_descriptor import ReturnType
from tweeql.function_registry import FunctionInformation, FunctionRegistry
from tweeql.query_runner import QueryRunner
from pyklout import Klout, KloutError

class Influence():
    return_type = ReturnType.FLOAT

    @staticmethod
    def factory():
        return Influence().influence

    def influence(self, tuple_data, val):
        """
            Returns the klout influence of the val, which is a string (screen_name)
        """
        api = Klout(general_settings.KLOUT_KEY)
        data = api.identity(str(val), 'twitter')
        user_id = data['id']
        data = api.score(user_id)

        return data['score']

fr = FunctionRegistry()
fr.register("influence", FunctionInformation(Influence.factory, Influence.return_type))
