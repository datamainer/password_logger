import csv

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

    def menu(self):
        user_answer = None
        while user_answer != '0':
            print(""" 
1. add 
2. delete
3. show all

0. exit
                    """)

            user_answer = input('$: ')

            if user_answer == '1':
                self.add_log()
                print(self.table)

            elif user_answer == '2':
                self.clear()
                print(self.table)

            elif user_answer == '3':
                self.show_table()

            elif user_answer == '4':
                continue

            else:
                print('error')

    def add_log(self):
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
        
        print(self.log)

        self.add_log_to_table()

    def add_log_to_table(self):
        self.table.field_names = ['ID', 'SERVICE', 'LOGIN', 'PASSWORD']
        self.table.add_row(self.log)
        self.log.clear()

    def clear(self):
        with open('log.csv') as file:
            reader = csv.reader(file, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
            
            for row in reader:
                self.cash_log.append(row)
                self.table.add_row(row)
        
        user_row = input('enter row id: ')
        if user_row == 'all':
            file = open('log.csv', 'w')
            file.close()
            self.table.clear_rows()
            self.menu()

        try:
            self.cash_log.pop(int(user_row) - 1)
            self.table.clear_rows()
            
            for row in self.cash_log:
                self.table.add_row(row)

            with open('log.csv', 'w') as file:
                write = csv.writer(file)
                write.writerows(self.cash_log)
        except:
            print('enter a number!!!')
        self.cash_log.clear()

    def show_table(self):
        self.table.clear_rows()
        with open('log.csv') as file:
            reader = csv.reader(file, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                self.table.add_row(row)
        
        print(self.table)



if __name__ == '__main__':
    from prettytable import PrettyTable
    Logger().menu()
