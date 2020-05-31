#!/usr/bin/python3
import random
import smtplib
import collections


class Person:

    def __init__(self, name, email, link):
        self.name = name
        self.email = email
        self.link = link

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getLink(self):
        return self.link

    def __str__(self):
        return ("Name: " + self.name + "\n" +
                "Email: " + self.email + "\n" +
                "Link: " + self.link + "\n")


def createList():
    p = []
    p.append(Person("Dorothy", "noriea@bellsouth.net",
                    "https://imgur.com/Wg568PC"))
    p.append(Person("Nicholas", "nfnoriea@gmail.com",
                    "https://imgur.com/8KkLxa5"))
    p.append(Person("Nickenator", "noriea@bellsouth.net",
                    "https://imgur.com/tRjCUuo"))
    p.append(Person("Stephanie", "slnoriea@gmail.com",
                    "https://imgur.com/g2MX228"))
    return p


def match():
    ppl = createList()
    matches = {}
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
    tryagain = True
    while(tryagain):
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
        secret_link = getter.getLink()
        giver_email = ""
        i = 0
        while(i < len(p)):
            person = p[i]
            if person.getName() == giver:
                giver_email = person.getEmail()
            i += 1
        subject = "Christmas Stocking Pick for " + giver
        body = "Ho ho ho! Find out who your secret stocking recipent is here: \n"
        body += secret_link + "\n\n"
        body += "This email was automatically sent with the Noriea Family Stocking List Maker created by N. Noriea\n\n"

        send_gmail("nfnoriea", "",
                   giver_email, subject, body)
