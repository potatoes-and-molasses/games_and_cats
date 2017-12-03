import socket
import sys
import os
import random
import thread
import string
import time


USER = 'lolcat'
PASSWORD = 'dolphins'

a=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    a.bind(((socket.gethostbyname(socket.gethostname()),0xf00d))

except:
    print 'try again lol!'
    os.system('taskkill /f /im pythonw.exe')

a.listen(10)



opts = {'exit':'run away!','password_restore':'restoring passwords for users','clue':'very information, such detail, alabyrinth','logon': 'do you even password?','con_troll_panel':'change server settings','howtocrypto':'notlikethis','unimplemented_admin_feature':'//dont forget to delete','lemon_earldom':'one million years dungeon!'}
def exit(con,enc,dec):
    con.send(enc('okay bye\n'))
    con.close()
    
    
    
def callf(fname,con,enc,dec):
    
    if fname == dec('howtocrypto'):
        fname = 'howtocrypto'
    
    exec 'troll = {}(con,enc,dec)'.format(fname)
    
    return troll



def howtocrypto(con,enc,dec):

    return 'maybe write something that can consistently handle this encryption instead of deciphering it by hand, this is a disgrace:D by the way, all other functions are too cool and would not be your friend unless you encrypt your messages.'

def clue(con,enc,dec):

    return 'functions wrapper is being exec\'d with 3 params'

def password_restore(con,enc,dec):
    con.send(enc('username: \n'))
    dat = dec(con.recv(1024).replace('\n',''))
    if len(dat) > 6:
        return 'invalid username'
    elif USER != dat:
        return 'user does not exist'
    else:
        return 'password is {}'.format(PASSWORD)
    
def con_troll_panel(con,enc,dec):
    global opts
    con.send(enc('1: os command\n2: disband universe\n3: y so hax0r?\n4: add util\n5: to the time machine!\n6: contrived and deceitful nastiness\n'))
    dat = dec(con.recv(1024).replace('\n',''))
    if dat in [str(i) for i in range(1,7)]:
        if dat == '1':
            return 'lolno'
        elif dat == '2':
            con.send(enc('initiating destruction of the known universe...\n'))
            time.sleep(0.5)
            con.send(enc('deploying assasination squads...\n'))
            time.sleep(0.5)
            con.send(enc('securing cornflakes sales monopoly in the next world...\n'))
            time.sleep(0.5)
            con.send(enc('launching fun missiles of amusing yet devestating destruction...\n'))
            time.sleep(0.5)
            opts = {'password_restore':'restoring passwords for users','clue':'very information, such detail, alabyrinth','logon': 'do you even password?','con_troll_panel':'change server settings','howtocrypto':'notlikethis','unimplemented_admin_feature':'//dont forget to delete','lemon_earldom':'one million years dungeon!'}
            time.sleep(1)
            con.send(enc('error! user32.dll missing(which is weird, he said he will be back for lunch!). reverting time(cleaned utils)...\n'))
            time.sleep(1)
            return 'try again later?'
        elif dat == '3':
            return 'abcdefghi'
        elif dat == '4':
            con.send(enc('util name: \n'))
            dat = dec(con.recv(1024).replace('\n',''))
            
            con.send(enc('util description: \n'))
            dat2 = dec(con.recv(4096).replace('\n',''))

            con.send(enc('util jscode: \n'))
            waste = con.recv(4096).replace('\n','')

            if dat not in opts:

                opts[dat] = dat2
                return 'util added'
            else:

                return 'util already exists'
            return ''
        elif dat == '5':
            return 'not today!'
        elif dat == '6':
            return 'dont worry be happy'
            
    else:
        return 'id of requested operation is invalid!'
    
def lemon_earldom(con,enc,dec):
    return 'availble functions: {}'.format(','.join(opts))

def unimplemented_admin_feature(con,enc,dec):
    con.send(enc('could be fun if this was a thing, riiiight?\n'))
    dat = dec(con.recv(1024).replace('\n',''))
    if enc('yes') == dat:
        return 'too bad'
    elif enc('no') == dat:
        return 'nope!'
    elif enc('nope') == dat:
        return 'try adding some utils'
    else:
        return ''
def logon(con,enc,dec):

    con.send(enc('username: \n'))
    dat = dec(con.recv(1024).replace('\n',''))
    if USER == dat:
        con.send(enc('password: \n'))
        dat = dec(con.recv(1024).replace('\n',''))
        if PASSWORD == dat:
            return 'well done! you have logged on to this wonderous system of mystery! sadly, the system resources are currently funneled into operating a crucial application, outlook.exe, and hence cannot handle your logon request, try again later.\n\np.s. you win lol!!!(yes this is the end, quite anticlimatic was it not?)\n\nowait, there is a secret file in the directory of this script, find it!'
        else:
            return 'nope'
    else:
        return 'nope'
def lol(someone):

    replaces = {}
    unreplaces = {}
    shuffled = list(string.ascii_lowercase)
    random.shuffle(shuffled)
    
    for j,i in enumerate(string.ascii_lowercase):
        replaces[i] = shuffled[j]
        unreplaces[shuffled[j]] = i
    def enc(strn):
        return ''.join(map(lambda x: x if x not in replaces else replaces[x],strn))
    
    def dec(strn):
        return ''.join(map(lambda x: x if x not in unreplaces else unreplaces[x],strn))
    
    
    someone.send(enc('trying to decrypt this message is probably a silly and worthless idea, as no useful information regarding the passphrase is hidden here and the encryption changes on every connection, sorry! what makes this exhausting message even less interesting is the fact that it is written with bland words, has no jokes in it, and all in all is quite a drag to read\n'))

    while 1:
        for i in opts:
            someone.send(enc('{} - {}\n'.format(i,opts[i])))
        d = dec(someone.recv(4096).replace('\n',''))

        retn='nothing lol!\n'
        
        if(d in opts or d==dec('howtocrypto')):
            
            retn = callf(d,someone,enc,dec)

        someone.send(enc(retn))
        temp = someone.recv(1024)
        someone.send('\n'*10)
        

while 1:
    conn,o = a.accept()

    thread.start_new_thread(lol,(conn,))


a.close()
    
