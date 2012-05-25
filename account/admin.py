from account.models import SEAccount, SEUser, SEClientProfile, SEFeed, SERule, SEInbox, SEArchive
from django.contrib import admin

admin.site.register(SEAccount)
admin.site.register(SEUser)
admin.site.register(SEClientProfile)
admin.site.register(SEFeed)
admin.site.register(SERule)
admin.site.register(SEInbox)
admin.site.register(SEArchive)