#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QListWidget, QHBoxLayout, QVBoxLayout, QInputDialog, QMessageBox

import json


TEXT = 'текст'
TAGS = 'тэги'
FILENAME = 'notes.json'
SEARCH_TXT = 'Искать заметки по тэгу'
IN_PROGRESS_TXT = 'Сбросить поиск'

NOTES = {
    "Note Name": {
        TEXT: 'Some text',
        TAGS: ['tag1', 'tag2']
    }, 
    "Моя заметка": {
        TEXT: 'Иногда очень хочется помогать людям, а иногда - не очень',
        TAGS: ['помощь', 'жизнь']
    }, 
}


def write_notes(notes):
    with open(FILENAME, 'w') as file:
        json.dump(notes, file)


def read_notes():
    with open(FILENAME, 'r') as file:
        notes = json.load(file)
        return notes


def filter_dict(my_dict, value):
    filtered_dict = {}
    for item in my_dict:
        if value in my_dict[item][TAGS]:
            filtered_dict[item] = my_dict[item]
    return filtered_dict


def errorWindow(txt, title='Ошибка!'):
    msg_window = QMessageBox()
    msg_window.setWindowTitle(title)
    msg_window.setText(txt)
    msg_window.exec()


def show_notes():
    note_name = note_list.selectedItems()[0].text()
    notes = read_notes()
    txt = notes[note_name][TEXT]
    note_txt_field.setText(txt)
    tags = notes[note_name][TAGS]
    tag_list.clear()
    tag_list.addItems(tags)


def add_note():
    note_text, ok = QInputDialog.getText(main_window, 'Добавить заметку', 'Введите название заметки:')
    if ok:
        NOTES[note_text] = { TEXT: '', TAGS: [] }
        note_list.clear()
        tag_list.clear()
        note_list.addItems(NOTES)
        tag_list.addItems(NOTES[note_text][TAGS])
        write_notes(NOTES)


def delete_note():
    if note_list.selectedItems():
        note_name = note_list.selectedItems()[0].text()
        del NOTES[note_name]
        note_list.clear()
        tag_list.clear()
        note_list.addItems(NOTES)
        write_notes(NOTES)
    else:
        errorWindow('Заметка не выбрана!')


def save_note():
    if note_list.selectedItems():
        note_name = note_list.selectedItems()[0].text()
        note_text = note_txt_field.toPlainText()
        NOTES[note_name][TEXT] = note_text
        write_notes(NOTES)
    else:
        errorWindow('Заметка не выбрана!')


def search_by_tag():
    tag_text = tag_add_line.text()
    if tag_search_btn.text() == SEARCH_TXT and tag_text != '':
        tag_search_btn.setText(IN_PROGRESS_TXT)
        filtered_notes = filter_dict(NOTES, tag_text)
        note_list.clear()
        tag_list.clear()
        note_txt_field.clear()
        note_list.addItems(filtered_notes)
    elif tag_search_btn.text() == IN_PROGRESS_TXT:
        tag_search_btn.setText(SEARCH_TXT)
        note_list.clear()
        tag_list.clear()
        note_txt_field.clear()
        note_list.addItems(NOTES)


def add_tag():
    if note_list.selectedItems():
        note_name = note_list.selectedItems()[0].text()
        tag_text, ok = QInputDialog.getText(main_window, 'Добавить тэг', 'Введите тэги через пробел:')
        if ok:
            NOTES[note_name][TAGS] += tag_text.split(' ')
            tag_list.clear()
            tag_list.addItems(NOTES[note_name][TAGS])
            write_notes(NOTES)
    else:
        errorWindow('Заметка не выбрана!')


def delete_tag():
    if note_list.selectedItems():
        if tag_list.selectedItems():
            note_name = note_list.selectedItems()[0].text()
            tag_name = tag_list.selectedItems()[0].text()
            NOTES[note_name][TAGS].remove(tag_name)
            tag_list.clear()
            tag_list.addItems(NOTES[note_name][TAGS])
            write_notes(NOTES)
        else:
            errorWindow('Тэг не выбран!')
    else:
        errorWindow('Заметка не выбрана!')


#write_notes(NOTES)
NOTES = read_notes()

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('SmartNotes')
main_window.resize(400, 400)

note_txt = QLabel('Список заметок')
tag_txt = QLabel('Список тэгов')

note_create_btn = QPushButton('Создать заметку')
note_create_btn.clicked.connect(add_note)

note_delete_btn = QPushButton('Удалить заметку')
note_delete_btn.clicked.connect(delete_note)

note_save_btn = QPushButton('Сохранить заметку')
note_save_btn.clicked.connect(save_note)

tag_attach_btn = QPushButton('Добавить к заметке')
tag_attach_btn.clicked.connect(add_tag)

tag_detach_btn = QPushButton('Открепить от заметки')
tag_detach_btn.clicked.connect(delete_tag)

tag_search_btn = QPushButton(SEARCH_TXT)
tag_search_btn.clicked.connect(search_by_tag)

note_txt_field = QTextEdit()

note_list = QListWidget()
note_list.addItems(NOTES)
note_list.itemClicked.connect(show_notes)

tag_list = QListWidget()
tag_add_line = QLineEdit()

note_btns_layout = QHBoxLayout()
note_btns_layout.addWidget(note_create_btn)
note_btns_layout.addWidget(note_delete_btn)

tag_btns_layout = QHBoxLayout()
tag_btns_layout.addWidget(tag_attach_btn)
tag_btns_layout.addWidget(tag_detach_btn)

management_layout = QVBoxLayout()
management_layout.addWidget(note_txt)
management_layout.addWidget(note_list)
management_layout.addLayout(note_btns_layout)
management_layout.addWidget(note_save_btn)
management_layout.addWidget(tag_txt)
management_layout.addWidget(tag_list)
management_layout.addWidget(tag_add_line)
management_layout.addLayout(tag_btns_layout)
management_layout.addWidget(tag_search_btn)

main_layout = QHBoxLayout()
main_layout.addWidget(note_txt_field)
main_layout.addLayout(management_layout)

main_window.setLayout(main_layout)

main_window.show()
app.exec_()