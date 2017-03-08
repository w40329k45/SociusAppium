#coding=utf-8
import random
import datetime

class AccountHelper():
    # max < length of 9
    domains = ["gmail.com","aol.com","mail.com","yahoo.com","soocii.me"]

    def __init__(self):
        self.datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.name = "autoqa{}".format(self.datetime)
        self.domain = self.domains[random.randint(0,len(self.domains)-1)]

    @property
    def name(self):
        return self.name

    @property
    def email(self):
        return "{}@{}".format(self.name, self.domain)
