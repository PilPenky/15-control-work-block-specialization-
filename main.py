from datetime import datetime
import json
import os
from datetime import datetime, date

filename = 'Notes.json'

def showAllNotes(filename):
    dataArr = []
    with open(filename, 'r') as f:
        for line in f:
            item = line.split(sep = " ")
            item = line.replace('{','').replace('}','').replace('[','').replace(']','').replace('"','')
            dataArr.append(item)
        print(*dataArr)


def cls():
    os.system('CLS')


def addNote(filename):
    id = searchNextId(filename)
    header = input("Введите название заметки: ")
    noteBody = input("Введите тело заметки: ")
    dt = dateAndTime().strftime("%Y-%m-%d %H:%M:%S")
    
    new_data = {'id': id, 'Header': header, 'Note Body': noteBody, 'Date/Time': dt} #создали переменную, включающую в себя данные, которые мы хотим добавить в уже имеющийся файл
    with open(filename, encoding='utf8') as f: #Открываем файл
        data = json.load(f) #Получаем все данные из файла (вообще все, да)
    data['Note'].append(new_data) #Добавляем данные
    with open(filename, 'w', encoding='utf8') as outfile: #Открываем файл для записи
        json.dump(data, outfile, ensure_ascii=False, indent=2) #Добавляем данные (все, что было ДО добавления данных + добавленные данные)


def searchNextId(filename):
    with open(filename, encoding='utf8') as f: #Открываем файл
        data = json.load(f) #Получаем все данные из файла (вообще все, да)
    
    index = len(data['Note'])
    id = data['Note'][index-1]['id']
    return id + 1


def changingNote(filename):
    showAllNotes(filename)
    idNote = int(input("Введите id заметки, которую хотите изменить: "))
    idNote -= 1
    newHeader = input("Введите новое название заметки: ")
    newNoteBody = input("Введите новое тело заметки: ")
    dt = dateAndTime().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, encoding='utf8') as f:
        data = json.load(f)
    
    new_data = {'id': idNote+1, 'Header': newHeader, 'Note Body': newNoteBody, 'Date/Time': dt}
    data.get("Note")[idNote] = new_data

    with open(filename, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def removeNote(filename):
    showAllNotes(filename)
    idNote = int(input("Введите id заметки, которую хотите удалить: "))
    idNote -= 1
    with open(filename, encoding='utf8') as f:
        data = json.load(f)

    del data['Note'][idNote]
    with open(filename, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    
    changingId(filename)
    cls()
    print("Заметка с id", idNote+1, "успешно удалена.")


def changingId(filename):
    with open(filename, encoding='utf8') as f:
        data = json.load(f)
    
    index = len(data['Note'])
    id = 1
    for i in range(0, index):
        data['Note'][i]['id'] = id
        id += 1

    with open(filename, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)    


def filterNewOld(filename):
    with open(filename, encoding='utf8') as f:
        data = json.load(f)

    for i in range(0, len(data['Note'])-1):
        for j in range(0, len(data['Note'])-1):
            if(data.get("Note")[j]["Date/Time"] < data.get("Note")[j+1]["Date/Time"]):
                tempIPlus1 = {'id': data.get("Note")[j+1]["id"], 'Header': data.get("Note")[j+1]["Header"], 'Note Body': data.get("Note")[j+1]["Note Body"], 'Date/Time': data.get("Note")[j+1]["Date/Time"]}
                tempI = {'id': data.get("Note")[j]["id"], 'Header': data.get("Note")[j]["Header"], 'Note Body': data.get("Note")[j]["Note Body"], 'Date/Time': data.get("Note")[j]["Date/Time"]}
            
                data.get("Note")[j+1] = tempI
                data.get("Note")[j] = tempIPlus1

                with open(filename, "w", encoding="utf8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
    changingId(filename)
    cls()
    showAllNotes(filename)


def filterOldNew(filename):
    with open(filename, encoding='utf8') as f:
        data = json.load(f)

    for i in range(0, len(data['Note'])-1):
        for j in range(0, len(data['Note'])-1):
            if(data.get("Note")[j]["Date/Time"] > data.get("Note")[j+1]["Date/Time"]):
                tempIPlus1 = {'id': data.get("Note")[j+1]["id"], 'Header': data.get("Note")[j+1]["Header"], 'Note Body': data.get("Note")[j+1]["Note Body"], 'Date/Time': data.get("Note")[j+1]["Date/Time"]}
                tempI = {'id': data.get("Note")[j]["id"], 'Header': data.get("Note")[j]["Header"], 'Note Body': data.get("Note")[j]["Note Body"], 'Date/Time': data.get("Note")[j]["Date/Time"]}
            
                data.get("Note")[j+1] = tempI
                data.get("Note")[j] = tempIPlus1

                with open(filename, "w", encoding="utf8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
    changingId(filename)
    cls()
    showAllNotes(filename)


def dateAndTime():
    today = datetime.today()
    return today


def searchDate(filename):
    with open(filename, encoding='utf8') as f:
        data = json.load(f)

    searchStrDate = input("Введите дату создания (изменения) заметки для поиска.\n" +
    "Дата указывается в формате: <<год-месяц-число>>: ")
    noRes = 0 
    for i in range(0, len(data['Note'])):
        onlyDate = data.get("Note")[i]["Date/Time"]
        dateSpl = onlyDate.split(sep = " ")
        
        if(dateSpl[0] == searchStrDate):
            resNote = data.get("Note")[i]
            trans_table = {ord('\'') : None, ord('{') : None, ord('}') : None}
            res = str(resNote).translate(trans_table)
            resSpl = res.split(sep = ", ")
            for i in range(0, len(resSpl)):
                print(resSpl[i])
                noRes += 1
    if (noRes == 0): 
        cls()
        print("Поиск по введенной дате не дал результатов.")


def showSpecificNote(filename):
    with open(filename, encoding='utf8') as f:
        data = json.load(f)

    showAllNotes(filename)
    idNoteShow = int(input("Введите id заметки, которую хотите просмотреть: "))
    cls()
    noRes = 0 

    for i in range(0, len(data['Note'])):
        if(data.get("Note")[i]["id"] == idNoteShow):
            resNote = data.get("Note")[i]
            trans_table = {ord('\'') : None, ord('{') : None, ord('}') : None}
            res = str(resNote).translate(trans_table)
            resSpl = res.split(sep = ", ")
            for i in range(0, len(resSpl)):
                print(resSpl[i])
                noRes += 1
    if (noRes == 0): 
        cls()
        print("Заметки с id", idNoteShow, "не существует.")


def menu():
    flag = True
    while(flag):
        try:
            cls()
            print('1 - Показать все заметки')
            print('2 - Добавить заметку')
            print('3 - Изменить заметку')
            print('4 - Удалить заметку')
            print('5 - Поиск по дате')
            print('<<Для закрытия программы укажите \"0\">>: ')

            user_operation = int(input('<<Укажите нужный пункт>>: '))
            if user_operation == 1:
                cls()
                showAllNotes(filename)
                print("Для сортировки заметок от новых к старым по дате создания/изменения, нажмите 1\n"
                "Для сортировки заметок от старых к новым по дате создания/изменения, нажмите 2\n"
                "Для вывода на экран определенную запись, нажмите 3\n\n"
                "Для возврата в главное меню, нажмите 0.")

                userNum = int(input('<<Укажите нужный пункт>>: '))
                if userNum == 1:
                    filterNewOld(filename)
                elif userNum == 2:
                    filterOldNew(filename)
                elif userNum == 3:
                    cls()
                    showSpecificNote(filename)
                elif userNum == 0:
                    continue
                else:
                    print("Ошибка! Введите число из списка.") 

                input("Нажмите любую кнопку для возврата в главное меню.")
            elif user_operation == 2: 
                cls()
                addNote(filename)
                input("Нажмите любую кнопку для возврата в главное меню.")
            elif user_operation == 3:
                cls()
                changingNote(filename)
                input("Нажмите любую кнопку для возврата в главное меню.")
            elif user_operation == 4:
                cls()
                removeNote(filename)
                input("Нажмите любую кнопку для возврата в главное меню.")
            elif user_operation == 5:
                cls()
                searchDate(filename)
                input("Нажмите любую кнопку для возврата в главное меню.")
            elif user_operation == 0:
                flag = False
        except ValueError:
            print("Ошибка! Введите число из списка.")

menu()