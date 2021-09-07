import csv
import pickledb
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich import box
from rich import print
from rich.panel import Panel
from rich.text import Text
import os 
from time import sleep

class Logger(object):
    def __init__(self):
        # лог для добавления в красивую таблицу 
        self.log = []
        # сама таблица
        self.table = PrettyTable()
        # номер строки 
        self.id = 0

        # лог записываться из таблицы для удаления нужных строк
        # затем с него перезаписывается таблица
        self.cash_log = []
        self.db = pickledb.load('login.db', True)

        self.console = Console()

        # создание таблицы
        self.table2 = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        self.table2.add_column('ID', style='dim', width=12)
        self.table2.add_column('SERVICE')
        self.table2.add_column('LOGIN')
        self.table2.add_column('PASSWORD')

    def login(self):
        # очистка терминала
        os.system('cls' if os.name == 'nt' else 'clear')

        new_login = Panel(Text("Wlcome to program\nprogram made by datamainer", justify="center"))
        if not self.db.exists('login'):
            print(new_login)
            self.db.set('login','username')
            self.db.set('password', input('create password: '))
            self.menu()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            if input('enter your password: ') != self.db.get('password'):
                print('error, try again')
                self.login()    

        self.menu()

    def menu(self):
        user_answer = None
        while user_answer != '4':
            os.system('cls' if os.name == 'nt' else 'clear')

            meun_txt = """ 
# Password Logger

1. add
2. delete
3. show all

0. exit
                    """
            
            markdown = Markdown(meun_txt)
            self.console.print(markdown)
            user_answer = input('$: ')

            if user_answer == '1':
                self.add_log()
                self.console.print(self.table2)
                sleep(1)

            elif user_answer == '2':
                self.clear()
                self.console.print(self.table2)
                sleep(1)

            elif user_answer == '3':
                self.show_table()

            else:
                print('error')
    
    def create_clean_tables(self):
        self.table2 = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        self.table2.add_column('ID', style='dim', width=12)
        self.table2.add_column('SERVICE')
        self.table2.add_column('LOGIN')
        self.table2.add_column('PASSWORD')


    def add_log(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        user_service = input('service: ')
        user_login = input('enter login: ')
        user_password = input('enter enter password: ')

        self.log.append(str(self.id))
        self.log.append(user_service)
        self.log.append(user_login)
        self.log.append(user_password)

        self.id += 1

        write_log = []
        write_log.append(self.log)

        log_file = open('log.csv', 'a')

        with log_file:
            writer = csv.writer(log_file)
            writer.writerows(write_log)
        
        self.add_log_to_table()

    def add_log_to_table(self):
        self.table2.add_row(*self.log)
        self.log.clear()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        self.create_clean_tables()
        with open('log.csv') as file:
            reader = csv.reader(file, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
            
            for row in reader:
                self.cash_log.append(row)
                self.table2.add_row(*row)
                # self.table.add_row(row)

        self.console.print(self.table2)

        user_row = input('enter row id: ')
        if user_row == 'all':
            file = open('log.csv', 'w')
            file.close()
            self.create_clean_tables()
            self.menu()

        try:
            self.cash_log.pop(int(user_row) - 1)
            self.create_clean_tables()

            for row in self.cash_log:
                self.table2.add_row(*row)

            with open('log.csv', 'w') as file:
                write = csv.writer(file)
                write.writerows(self.cash_log)
        except:
            print('enter a number!!!')
        self.cash_log.clear()

    def show_table(self):
        self.create_clean_tables()
        with open('log.csv') as file:
            reader = csv.reader(file, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                self.table2.add_row(*row)

        self.console.print(self.table2)
        input('press enter to go back')
        

if __name__ == '__main__':
    from prettytable import PrettyTable
    Logger().login()
