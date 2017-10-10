#!/Users/lawerencelee/anaconda/bin/python
from collections import OrderedDict
import datetime
import sys
import os

from peewee import *


db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db
        
def initalize():
    db.connect()
    db.create_tables([Entry], safe=True)

def __clear():
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")
    
def menu_loop():
    '''Show The Menu.'''
    choice = None
    
    while choice != 'q':
        __clear()
        print('Enter q to QUIT')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\nAction: ').lower().strip()
        
        if choice in menu:
            menu[choice]()
            
def add_entry():
    """Add an Entry."""
    __clear()
    print('Enter your entry. Press ctrl+d when finished.')
    data = sys.stdin.read().strip()
    
    if data:
        if input('\nSave entry? [Y/n]: ').lower() != 'n':
            Entry.create(content=data)
            input("\nSaved Successfully, press ENTER to Continue. ")

def view_entries(search_query=None):
    """View Previous Entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    
    for entry in entries:
        __clear()
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content, '\n\n')
        print('='*len(timestamp))
        print('n) Next Entry')
        print('d) Delete Entry')
        print('q) Main Menu')
        
        next_action = input('\nAction: [N/d/q] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entries(entry)
            
def search_entries():
    '''Search Via Keyword'''
    __clear()
    view_entries(input('Search query: '))
        
def delete_entries(entry):
    """Delete Entries"""
    if input('\nAre you sure? [y/N] ').lower() == 'y':
        entry.delete_instance()
        __clear()
        input('Entry Deleted, press Enter to Continue. ')

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])


if __name__ == '__main__':
    initalize()
    menu_loop()