#!/usr/bin/python3
import random
import smtplib
import collections


class Person:

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def __str__(self):
        return ("Name: " + self.name + "\n" +
                "Email: " + self.email)


def createList():
    p = []
    p.append(Person("Dorothy", "nfnoriea@gmail.com"))
    p.append(Person("Nicholas", "nfnoriea@gmail.com"))
    p.append(Person("Nick Jr. i.e. The Nickenator", "nfnoriea@gmail.com"))
    p.append(Person("Stephanie", "nfnoriea@gmail.com"))
    p.append(Person("Jennifer", "nfnoriea@gmail.com"));
    return p


def match():
    
    # ppl = persons left that need to be picked to give a stocking
    ppl = createList()
    
    matches = {}

    # pleft = persons left that need to be picked to get a stocking
    pleft = ppl.copy()

    while(len(pleft) > 1):
        
        giver = ppl[random.randint(0, len(ppl)-1)]
        
        getter = pleft[random.randint(0, len(pleft)-1)]

        if(giver.getName() == getter.getName()):
            continue
        else:
            matches.update({giver.getName(): getter})
            pleft.remove(getter)
            ppl.remove(giver)
    if(ppl[0].getName() == pleft[0].getName()):
        return False
    else:
        matches.update({ppl[0].getName(): pleft[0]})
        return matches


def getMatches():

    availableGivers = createList()
    availableRecipients = availableGivers.copy()
    
    # there is no guarantee that the last match to be picked isn't the same person
    # so when there is only one match left, must check if that giver/recipient is the same person


    while(True):

    matches = {} # dictionary of person:person




    while(True):
        m = match()
        if(isinstance(m, collections.Mapping)):
            return m


def send_gmail(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """From: /%s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("Successfully sent email.")
    except:
        print("Failed to send email.")


if __name__ == '__main__':
    p = createList()
    m = getMatches()
    for match in m:
        giver = match
        getter = m[match]
        giver_email = ""
        i = 0
        while(i < len(p)):
            person = p[i]
            if person.getName() == giver:
                giver_email = person.getEmail()
            i += 1
        subject = "Christmas Stocking Pick for " + giver
        body = "Ho ho ho! Your 2020 secret stocking recipent is:  <b>" + getter.getName() + "\n\n"
        body += "This email was automatically sent with the Noriea Family Stocking List Maker created by N. Noriea\n\n"

        send_gmail("nfnoriea", "",
                   giver_email, subject, body)
