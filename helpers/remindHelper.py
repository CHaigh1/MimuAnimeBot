def reminders():
    remindersString = ''
    with open('reminders.txt', 'r') as f:
        remindersString = f.read()
    return remindersString

def addReminder(message):
    with open('reminders.txt', 'a') as f:
        f.write('\n' + message)

def removeReminder(index):
    remindersByLine = []
    with open('reminders.txt', 'r') as f:
        remindersByLine = f.readlines()

    del remindersByLine[index]
    
    with open('reminders.txt', 'w') as f:
        f.writelines(remindersByLine)