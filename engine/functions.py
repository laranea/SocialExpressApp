'''
Created on May 19, 2012

@author: kristof.leroux@gmail.com
'''
# -*- coding: utf-8 -*-
import general_settings
from tweeql.exceptions import TweeQLException
from tweeql.field_descriptor import ReturnType
from tweeql.function_registry import FunctionInformation, FunctionRegistry
from tweeql.query_runner import QueryRunner
from pyklout import Klout, KloutError
from language import LangDetect

class Url():
    return_type = ReturnType.STRING

    @staticmethod
    def factory():
        return Url().get_url

    def get_url(self, tuple_data, val):
        tuple_data['screen_name'] = tuple_data['author'].screen_name
        return 'http://twitter.com/%(screen_name)s/status/%(id)s' % tuple_data

fr = FunctionRegistry()
fr.register("url", FunctionInformation(Url.factory, Url.return_type))

class Entities():
    return_type = ReturnType.STRING

    @staticmethod
    def factory():
        return Entities().get_entities

    def get_entities(self, tuple_data, val):
        values = tuple_data['entities']
        value = values[val]
        if val == 'hashtags':
            return ','.join(list(set([v['text'].lower() for v in value])))
        elif val == 'user_mentions':
            return ','.join([v['screen_name'] for v in value])

fr = FunctionRegistry()
fr.register("entities", FunctionInformation(Entities.factory, Entities.return_type))


class Influence():
    return_type = ReturnType.FLOAT

    @staticmethod
    def factory():
        return Influence().get_influence

    def get_influence(self, tuple_data, screen_name):
        """
            Returns the klout influence of the val, which is a string (screen_name)
        """
        try:
            api = Klout(general_settings.KLOUT_KEY)
            data = api.identity(str(screen_name), 'twitter')
            user_id = data['id']
            data = api.score(user_id)
            return data['score']
        except KloutError:
            return -1

fr = FunctionRegistry()
fr.register("influence", FunctionInformation(Influence.factory, Influence.return_type))

class Language():
    return_type = ReturnType.STRING
    
    @staticmethod
    def factory():
        return Language().get_language
    
    def get_language(self, tuple_data, text):
        """
        """
        ld = LangDetect()
        return ld.detect(text)
    
fr = FunctionRegistry()
fr.register("language", FunctionInformation(Language.factory, Language.return_type))
    
    