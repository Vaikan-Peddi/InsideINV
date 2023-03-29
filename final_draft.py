import pandas as pd
import numpy as np
import os
from time import sleep
from tabulate import tabulate
from operator import itemgetter
import getpass
import plotext as plt
from datetime import datetime

#initialising the program by reading the external files
pwds = pd.read_excel('pwd.xlsx')
comps = pd.read_excel('components.xlsx')

usernames = []
passwords = []
fnames = []
coms = []

for i in range(0, len(pwds)):
    usernames.append(str(pwds['EMP_ID'].iloc[i]))
    passwords.append(pwds['PWD'].iloc[i])
    fnames.append(pwds['FNAME'].iloc[i])

for i in range(0, len(comps)):
    coms.append([comps['COMPONENT'].iloc[i], comps['COUNT'].iloc[i]])

def valid(uname, passwd):
    try:
        index = usernames.index(uname)
    except:
        return False
    if passwd == passwords[index]:
        return True
    else:
        return False

def login():
    os.system('cls')
    print("Employee Login Page")
    print()
    idd=str(input('InsideID: \n>>>'))
    pw=getpass.getpass('Password:\n>>> ')
    if valid(idd, pw):
        os.system('cls')
        if idd=='admin':
            admin()
        else:
            dashboard(idd)
    else:
        print('Try Again!!!')
        input('>>> Press any key to continue')
        login()

def comp_list():
    comp_table = tabulate(coms, tablefmt='fancygrid')
    print('Components and their availability: ')
    print(comp_table)

def dashboard(uid):
    os.system('cls')
    print('----------Inside '+uid+'-----------')
    graph()
    print()
    print()

    k=str(input('>>>'))
    if k=='logout':
        os.system('cls')
        homepage()
    elif k == 'add':
        add_comp(uid)
        upd_db()
        dashboard(uid)
    elif k == 'update':
        upd_comp(uid)
        upd_db()
        dashboard(uid)
    elif k == 'remove':
        rem_comp(uid)
        upd_db()
        dashboard(uid)
    elif k == 'save':
        upd_db()
        dashboard(uid)
    elif k =='logs':
        show_logs(uid)
        input('>>> Press any key to continue')
        dashboard(uid)
    elif k=='HELP':
        print("These are the commands that are active in this version: ")
        print("UNIVERSAL:")
        print("\tHELP: To open this window")
        print("HOMEPAGE:")
        print("\tlogin: To open login page")
        print("\texit: To exit InsideINV")
        print("DASHBOARD:")
        print("\tlogout: logout and getback to the homepage")
        print("\tadd: Add a new component")
        print("\tupdate: Update a component")
        print("\tremove: Delete a component")
        print("\tlogs: Your current logs til date")
        print("\tsave: InsideINV autosaves after every operation but for Ctrl+S nerds like me!")
        input("Enter any key to get back!")
        dashboard(uid)
    else:
        print('That is a wrong command, enter HELP for knowing about InsideINV commands')
        upd_db()
        input('>>> Press any key to continue')
        dashboard(uid)

def admin():
    os.system('cls')
    print('----------Inside ADMIN-----------')
    graph()
    print()
    print()
    k=str(input('>>>'))
    if k=='logout':
        os.system('cls')
        homepage()
    elif k == 'add':
        add_comp('admin')
        upd_db()
        admin()
    elif k == 'update':
        upd_comp('admin')
        upd_db()
        admin()
    elif k == 'remove':
        rem_comp('admin')
        upd_db()
        admin()
    elif k == 'save':
        upd_db()
    elif k =='logs':
        uid=str(input('Enter the id you want the logs of:'))
        show_logs(uid)
        input('>>> Press any key to continue')
        admin()
    elif k=='HELP':
        print("These are the commands that are active in this version: ")
        print("UNIVERSAL:")
        print("\tHELP: To open this window")
        print("HOMEPAGE:")
        print("\tlogin: To open login page")
        print("\texit: To exit InsideINV")
        print("DASHBOARD:")
        print("\tlogout: logout and getback to the homepage")
        print("\tadd: Add a new component")
        print("\tupdate: Update a component")
        print("\tremove: Delete a component")
        print("\tlogs: Your current logs til date")
        print("\tsave: InsideINV autosaves after every operation but for Ctrl+S nerds like me!")
        input("Enter any key to get back!")
        admin()
    else:
        print('That is a wrong command, enter HELP for knowing about InsideINV commands')
        upd_db()
        input('>>> Press any key to continue')
        admin()

def add_comp(uid):
    print('Component Name:')
    name=str(input())
    if name in list(map(itemgetter(0), coms)):
        print('Component alrady on board, try calling update!')
        input('>>> Press any key to continue')
    else:
        comp_2=str(input('Enter ' + name + ' count: '))
        coms.append([name, int(comp_2)])
        logger(uid, 1, int(comp_2), name)

def upd_comp(uid):
    print('Component to update:')
    name = str(input())
    if name in list(map(itemgetter(0), coms)):
        index = list(map(itemgetter(0), coms)).index(name)
        com_cnt = coms[index][1]
        sub_func=str(input('>>>give or take?\n'))
        if sub_func=='give':
            diff=int(input('>>>value: '))
            new_cnt=com_cnt+diff
        elif sub_func=='take':
            diff=int(input('>>value: '))
            new_cnt=com_cnt-diff
        coms[index][1] = int(new_cnt)
        logger(uid, 3, int(new_cnt), name)
    else:
        print('Component not on board, try calling add')
        input('>>> Press any key to continue')

def rem_comp(uid):
    print('Component to remove: ')
    name = str(input())
    index=-1
    if name in list(map(itemgetter(0), coms)):
        index = list(map(itemgetter(0), coms)).index(name)
        coms.remove(coms[index])
        logger(uid, 2, 0, name)
    else:
        print('Component already absent!')
        input('>>> Press any key to continue')

def graph():
    coms_0 = []
    coms_1 = []
    for ele in range(0,len(coms)):
        coms_0.append(coms[ele][0])
        coms_1.append(coms[ele][1])
    plt.simple_bar(coms_0, coms_1, width = 100, title = 'Components')
    plt.show()

def upd_db():
    data = np.array(coms)
    new_df = pd.DataFrame(data, columns=['COMPONENT', 'COUNT'])
    comps=new_df
    comps.to_excel('components.xlsx', index=False)

def homepage():
    print('-----------InsideINV-----------')
    print('\n\n')
    print("\tWelcome to InsideFPV's Inventory!")
    print('\n\n')
    graph()
    print()
    while True:
        ptr=str(input('>>>'))
        if ptr=='login':
            login()
        elif ptr=='exit':
            print('Closing the application!')
            sleep(1)
            exit()
        elif ptr=='HELP':
            print("These are the commands that are active in this version: ")
            print("UNIVERSAL:")
            print("\tHELP: To open this window")
            print("HOMEPAGE:")
            print("\tlogin: To open login page")
            print("\texit: To exit InsideINV")
            print("DASHBOARD:")
            print("\tlogout: logout and getback to the homepage")
            print("\tadd: Add a new component")
            print("\tupdate: Update a component")
            print("\tremove: Delete a component")
            print("\tlogs: Your current logs til date")
            print("\tsave: InsideINV autosaves after every operation but for Ctrl+S nerds like me!")
            input("Enter any key to get back!")
        else:
            print("Wrong InsideCODE, try HELP for commands")

def logger(uid, case, val, comp):
    filename = uid+'.txt'
    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    file = open(filename, append_write)
    if case==1:
        file.write(str(datetime.now())+': '+'added '+comp+' of '+str(val)+' count.\n')
    elif case==2:
        file.write(str(datetime.now())+': '+'deleted '+comp+'\n')
    elif case==3:
        file.write(str(datetime.now())+': '+'modified '+comp+' to '+str(val)+' count.\n')
    file.close()

def show_logs(uid):
    filename = uid+'.txt'
    try:
        file = open(filename, 'r')
        full_str = file.read()
        full_str=full_str.rstrip('\n')
        tmp=full_str.split('\n')
        tmp_recent=tmp[-5:]
        tmp_recent.reverse()
        for line in tmp_recent:
            print('>>> '+line)
        print('>>> open log files in your source folder for more history')
        file.close()
    except:
        print('You have not logged any changes, please make any to check.')
    
homepage()

