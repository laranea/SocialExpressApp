from controllers.controller1 import Controller1
from controllers.controller2 import Controller2
from controllers.users import *
from kiss.core import events as Event
from kiss.models import SqliteDatabase, MySQLDatabase
from kiss.core.exceptions import InternalServerError


options = {
	"application": {
		"address": "127.0.0.1",
		"port": 8080
	},
	"urls": {
		"": Controller1,
		"users": {
			"(?P<user>\w+)": Controller2
		},
		"2": {
			"3": Controller1,
			"4": Controller2
		},
        "login": UserLogin,
        "wizard": UserProfile,
        "registration": UserRegistration,
        "register": UserRegister,
	},
	"views": {
		"templates_path": "views.templates",
		"static_path": "views.static"
	},
	"events": {
		Event.ApplicationStarted: Controller2.application_after_load,
		InternalServerError.code: Controller2.internal_server_error
	},
	"models": {
		"engine": MySQLDatabase,
		"host": "localhost",
		"database": 'socialexpress',
		"user": 'root',
		"passwd": 'elleke'
	}
}

