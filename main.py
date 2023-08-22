import json
import os
from time import sleep
import base64
from requests import post
# from utils.settings import CLIENT_SECRET , CLIENT_ID

def getJSON(name):
    return f'data/{name}.json'

def read_data(filename):
    try:
        with open(filename , 'r') as f:
            return json.load(f)
    except:
        return {}
    
def write_data(data , filename):
    with open(filename , 'w') as f:
        json.dump(data, f, indent=4)



class CLLD():
    def __init__(self, name=None):
        self.name = name

    def __details(self):
        while True: 
            if os.path.exists(getJSON(self.name)):
                print('Theres an account already , Login back or try a different user name .')
                sleep(1)
                break
            else:
                password = input('Create a password  : ')
                if len(password) < 5:
                    print('Too short password!')
                    continue
                print('Creating...')
                filepath = getJSON(self.name)
                data = read_data(filename=filepath)
                data['password'] = password
                write_data(data= data,filename=filepath)
                sleep(1)
                print('Your account has been successfully created !')
                sleep(1)
                break  
    
    def __loginInfo(self):
        data = read_data(getJSON(self.name))
        if os.path.exists(getJSON(self.name)):
            password = input('Enter your password : ')
            if data['password'] != password:
                print('Invalid password ! Try again')
                sleep(1)
                
            else:
                acuser = read_data(filename='data/active/acuser.json')
                acuser['active'] = self.name
                write_data(data=acuser , filename='data/active/acuser.json')
                sleep(1)
                print('Logged in successfully')
                sleep(1)
                
        else:
            print('Theres no valid account !')
            sleep(1)
                
    def __logoutInfo(self):
        data = read_data(getJSON(self.name))
        if os.path.exists(getJSON(self.name)):
            
            password = input('Enter your password : ')
            if data['password'] != password:
                print('Invalid password ! Try again')
                sleep(1)
            else:
                acuser = read_data(filename='data/active/acuser.json')
                acuser['active'] = None
                write_data(data=acuser , filename='data/active/acuser.json')
                sleep(1)
                print('Logged out successfully')
                sleep(1)
        else:
            print('Incorrect name ')
            sleep(1)
        
    def __deleteInfo(self):
        data = read_data(getJSON(self.name))
        if os.path.exists(getJSON(self.name)):
            password = input('Enter your password: ')
            if data['password'] != password:
                print('Invalid password')
            else:
                print('Deleting...')
                os.remove(getJSON(self.name))
                acuser = read_data(filename='data/active/acuser.json')
                if acuser['active'] == self.name:
                    acuser['active'] = None
                    write_data(data=acuser , filename='data/active/acuser.json')
                sleep(1)
                print('Your account has been deleted')
                sleep(1)
        else:
            print('Theres no valid account')
            sleep(1)

    def create(self):
        self.__details()

    def login(self):
        self.__loginInfo()
    
    def logout(self):
        self.__logoutInfo()

    def delete(self):
        self.__deleteInfo()


def main():
    
    print('\n\n\t\t================\n\t\t|    Anbify    |\n\t\t================')
    sleep(1)

    while True:

        if os.path.exists('data'):
            pass
        else:
            os.mkdir('data')

        acdata = read_data('data/active/acuser.json')
        
        print('\n\n * Create an account\n * Login\n * Logout\n * Delete account\n * Exit')
        opt = input('\nSelect(1-5): ')
        if opt == '1':
            while True:
                name = input('\nEnter your name : ')
                if any(char.isnumeric() for char in name):
                    print("Don't use numeric usernames")
                    continue
                if any(char.isupper() for char in name):
                    print('Use only lowercase letters !')
                    continue
                CLLD(name=name).create()
                break

        elif opt == '2':

            if os.path.exists('data/active'):
                if os.path.exists('data/active/acuser.json'):
                    pass
                else:
                    write_data(data={
                        "active": None,
                    } , filename='data/active/acuser.json')
            else:
                os.mkdir('data/active')
                write_data(data={
                        "active": None,
                    } , filename='data/active/acuser.json')
                
            updated_acdata = read_data(filename='data/active/acuser.json')
                
            
            if updated_acdata['active'] == None :
                while True:
                    name = input('\nEnter your name : ')
                    if any(char.isupper() for char in name):
                        print('Use only lowercase letters !')
                        continue
                    
                    CLLD(name=name).login()
                    break
            else:
                print('\nYou are already logged into another account')
                sleep(1)
        elif opt == '3':
        
            if os.path.exists('data/active') and os.path.exists('data/active/acuser.json') and 'active' in acdata and acdata['active'] != None:

                name = acdata['active']
                CLLD(name=name).logout()
                   
            else:
                print('\nYou are already logged out ')
                sleep(1)
        elif opt == '4':
            while True:
                name = input('\nEnter your name : ')
                if any(char.isupper() for char in name):
                    print('Use only lowercase letters !')
                    continue
                CLLD(name=name).delete()
                break
        elif opt == '5':
            print('\nThanks for using !')
            break
        elif opt.strip(' ') == '':
            continue
        else:
            print('\nIncorrect option !')
            break


if __name__ == '__main__':
    main()
