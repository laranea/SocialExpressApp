from kiss.models import Model, IntegerField, BooleanField, FloatField, CharField, TextField, DateTimeField, BooleanField, ForeignKeyField
# Create your models here.
class Account(Model):
    account_id = IntegerField()
    
    def __unicode__(self):
        return self.account_id
    
class User(Model):
    user_id = IntegerField()
    username = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = CharField(max_length=255)
    password = CharField(max_length=255)
    is_staff = BooleanField()
    is_active = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField()
    date_joined = DateTimeField()
    
    departement = CharField(max_length=255)
    account = ForeignKeyField(Account)
    #
    
    def __unicode__(self):
        return self.user_id
    
class ClientProfile(Model):
    twitter_username = CharField(max_length=255)
    twitter_password = CharField(max_length=255)
    user = ForeignKeyField(User)
    
    def __unicode__(self):
        return self.twitter_username
    
class Feed(Model):
    feed_id = IntegerField()
    text = CharField(max_length=255)
    screen_name = CharField(max_length=255)
    pub_date = DateTimeField('date published')
    influence_score = FloatField()
    sentiment_score = FloatField()
    reply = BooleanField()
    problem = BooleanField()
    praise = BooleanField()
    language = CharField(max_length=255)
    client_profile = ForeignKeyField(ClientProfile)
    TYPES = (
        (0, 'Twitter'),
        (1, 'Facebook'),
        (2, 'Linkedin')
    )

    feed_type = IntegerField(choices=TYPES, default=0)
    
    def __unicode__(self):
        return self.text
        
class Rule(Model):
    rule_id = IntegerField()
    if_clause = CharField(max_length=255)
    then_clause = CharField(max_length=255)
    action_clause = CharField(max_length=255)
    client_profile = ForeignKeyField(ClientProfile)
    TYPES = (
        (0, 'sentiment'),
        (1, 'mentions'),
    )

    rule_type = IntegerField(choices=TYPES, default=0)
    
    def __unicode__(self):
        return "if " + self.if_clause + " then " + self.then_clause + " do " + self.action_clause 
    
class SEInbox(Feed):
    pass

class SEArchive(Feed):
    pass

class Blog(Model):
    creator = CharField()
    name = CharField()
    
class Entry(Model):
    blog = ForeignKeyField(Blog)
    title = CharField()
    body = TextField()
    pub_date = DateTimeField()
    published = BooleanField(default=True)
