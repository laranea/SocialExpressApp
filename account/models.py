from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
class SEAccount(models.Model):
    account_id = models.IntegerField()
    
    def __unicode__(self):
        return self.account_id
    
class SEUser(User):
    departement = models.CharField(max_length=255)
    account = models.ForeignKey('SEAccount')
    objects = UserManager()
    
    def __unicode__(self):
        return self.__unicode__()
    
class SEClientProfile(models.Model):
    twitter_username = models.CharField(max_length=255)
    twitter_password = models.CharField(max_length=255)
    user = models.OneToOneField('SEUser')
    
    def __unicode__(self):
        return self.twitter_username
    
class SEFeed(models.Model):
    feed_id = models.IntegerField()
    text = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    influence_score = models.FloatField()
    sentiment_score = models.FloatField()
    reply = models.BooleanField()
    problem = models.BooleanField()
    praise = models.BooleanField()
    language = models.CharField(max_length=255)
    client_profile = models.ForeignKey('SEClientProfile')
    TYPES = (
        (0, 'Twitter'),
        (1, 'Facebook'),
        (2, 'Linkedin')
    )

    type = models.IntegerField(choices=TYPES, default=0)
    
    def __unicode__(self):
        return self.text
        
class SERule(models.Model):
    rule_id = models.IntegerField()
    if_clause = models.CharField(max_length=255)
    then_clause = models.CharField(max_length=255)
    action_clause = models.CharField(max_length=255)
    client_profile = models.ForeignKey('SEClientProfile')
    TYPES = (
        (0, 'sentiment'),
        (1, 'mentions'),
    )

    type = models.IntegerField(choices=TYPES, default=0)
    
    def __unicode__(self):
        return "if " + self.if_clause + " then " + self.then_clause + " do " + self.action_clause 
    
class SEInbox(SEFeed):
    pass

class SEArchive(SEFeed):
    pass