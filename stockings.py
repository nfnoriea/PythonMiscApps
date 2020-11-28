import random
import smtplib
import collections
from email.mime.text import MIMEText


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
    personList = []
    personList.append(Person("Dorothy ('The Dottie')", "noriea@bellsouth.net"))
    personList.append(Person("Nicholas ('The III')", "nfnoriea@gmail.com"))
    personList.append(Person("Nick Jr. ('The Nickenator')", "noriea@bellsouth.net"))
    personList.append(Person("Stephanie ('The Croaker')", "slnoriea@gmail.com"))
    personList.append(Person("Jennifer ('The Tater')", "jennifernorieazhou@gmail.com"))
    return personList


def getMatches():
    
    # there is no guarantee that the last match giver and recipient are different persons
    # so when there is only one match left, must check if that giver/recipient is the same person
    # if so, repeat entire match process
    # this can probably be refactored into a good selection algorithm if needed
    while(True):
        availableGivers = createList()
        availableRecipients = availableGivers.copy()
        matches = {} # dictionary of person:person

        # loop continuously while there is still people who need to get a stocking
        # create a match from list of people who haven't been picked to give a stocking
        while(len(availableRecipients) > 1):
            giver = availableGivers[random.randint(0,len(availableRecipients)-1)]
            recipient = availableRecipients[random.randint(0,len(availableRecipients)-1)]
            if(giver.getName() == recipient.getName()):
                continue
            else:
                matches.update({giver: recipient})
                availableRecipients.remove(recipient)
                availableGivers.remove(giver)
        
        # when there is only 1 recipient left, check if last recipient and last giver are the same
        if(availableGivers[0].getName() == availableRecipients[0].getName()):
            continue
        else:
            matches.update({availableGivers[0]: availableRecipients[0]})
            return matches


def send_gmail(user, pwd, giver, recipient):

    # Using MIMEText for html formatting rather than just text formatting
    body = "<html><body>Ho ho ho! Your 2020 secret stocking recipent is: <p style=\"color:red;\"><b>" + recipient.getName() + "</b></p></body></html>"

    myEmail = MIMEText(body, 'html')
    myEmail["From"] = user
    myEmail["To"] = recipient.getEmail()
    myEmail["Subject"] = "Christmas Stocking Pick for " + giver.getName()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, giver.getEmail(), myEmail.as_string())
        server.close()
        print("----------------  Successfully sent email.\n")
    except:
        print("----------------  Failed to send email.\n")


if __name__ == '__main__':
    m = getMatches()

    user = input("Enter Gmail:")
    pwd = input("Enter Gmail Password:")

    for match in m:
        giver = match
        recipient = m[match]
        send_gmail(user, pwd, giver, recipient)
