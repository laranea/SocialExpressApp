'''
Created on May 19, 2012

@author: kristof.leroux@gmail.com
'''
import general_settings
from pyklout import Klout, KloutError

class KloutInfluence(object):
    def __init__(self, twitter_screen_name):
        self.screen_name = twitter_screen_name
        
    def score(self):
        api = Klout(general_settings.KLOUT_KEY)
        data = api.identity(self.screen_name, 'twitter')
        user_id = data['id']
        data = api.score(user_id)
        return data['score']
    
    def influences(self):
        api = Klout(general_settings.KLOUT_KEY)
        data = api.identity(self.screen_name, 'twitter')
        user_id = data['id']
        return api.influences(user_id)
        
    def topics(self):
        api = Klout(general_settings.KLOUT_KEY)
        data = api.identity(self.screen_name, 'twitter')
        user_id = data['id']
        return api.topics(user_id)
 
if __name__ == '__main__':
    klout = KloutInfluence('laranea')
    print(klout.score())
    print(klout.influences())
    print(klout.topics())
    