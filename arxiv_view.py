#! /usr/bin/env python
from tkinter import (
    Tk, 
    Label, 
    Button, 
    Scrollbar,
    Listbox,
    RIGHT,
    LEFT,
    BOTH,
    Y,
    END,
    CENTER,
    PhotoImage,
    ttk,
)
import arxiv
import re
import os
import yaml
import time
import json
import subprocess

def get_pattern():
    return r'([0-9]){4}\.([0-9]){5}(-[0-9]+)?\.pdf'

def get_cfg():
    with open('/home/thomas/src/arxiv_view/config.yaml', 'r') as f:
        return yaml.load(f, yaml.Loader)

def get_arxiv_fpaths(cfg):
    pattern = get_pattern()
    return [
        x for x in os.listdir(cfg['download_dir'])
        if re.match(pattern, x) is not None
    ]

def get_previous():
    fpath = '/home/thomas/src/arxiv_view/titles.json'
    if os.path.exists(fpath):
        with open(fpath, 'r') as f:
            return json.load(f)
    else:
        return {}

def persist_result(titles):
    fpath = '/home/thomas/src/arxiv_view/titles.json'
    with open(fpath, 'w') as f:
        json.dump(titles, f)

def get_arxiv_id(arxiv_fpath):
    return arxiv_fpath[:10]

def get_arxiv_titles(arxiv_fpaths):
    print("Fetching title data through the arxiv package")
    print("If this is your first time to use arxiv_view or you've downloaded a lot of files")
    print("since the last time you used arxiv_view, this command may take a while")
    prev_titles = get_previous()
    titles = {}
    for fpath in arxiv_fpaths:
        if fpath in prev_titles: continue
        s = arxiv.Search(id_list=[get_arxiv_id(fpath)])
        titles_ = [x.title for x in s.results()]
        titles[fpath] = titles_
        time.sleep(0.1)
    for key, val in titles.items():
        prev_titles[key] = val
    print("Saving titles in ./titles.json")
    persist_result(prev_titles)
    titles = [(v[0],k) for (k,v) in prev_titles.items()]
    titles.sort()
    return titles

def parse_fname(data):
    fname, _ = data.split(' : ')
    return os.path.join(cfg['download_dir'], fname)

def run_evince(data):
    fpath = parse_fname(data)
    cmd = ['evince', fpath]
    p = subprocess.Popen(cmd)

cfg = get_cfg()

def warm_start():
    arxiv_fpaths = get_arxiv_fpaths(cfg)
    return get_arxiv_titles(arxiv_fpaths)

def main():
    titles = warm_start()
    fire_up_gui(titles)

def fire_up_gui(titles):            
    win = Tk()
    win.title('ARXIV VIEW')
    win.geometry('1200x500')
    # win.iconbitmap(r'/home/thomas/src/arxiv_view/arxiv.ico')
    win.tk.call('wm', 'iconphoto', win._w, PhotoImage(file='/home/thomas/src/arxiv_view/arxiv.gif'))
    s = ttk.Style()
    s.theme_use('clam')
    mylabel = Label(win, text='Arxiv Titles', font='30')
    mylabel.pack()
    label = Label(win)
    label.pack(side='bottom', fill='x')
    myscroll = Scrollbar(win)
    myscroll.pack(side=RIGHT, fill=Y)
    mytree = ttk.Treeview(win, column=('c1', 'c2'), show='headings', height=5, yscrollcommand=myscroll.set)
    mytree.column('# 1', anchor=CENTER, width=200)
    mytree.heading('# 1', text='File Name')
    mytree.column('# 2', anchor='w', width=800)
    mytree.heading('# 2', text='Title')
    for (title, arxiv_id) in titles:
        # mytree.insert(END, f'{key} : {val[0]}')
        mytree.insert('', 'end', text='1', values=(arxiv_id, title))
    mytree.pack(side='left', padx=30, fill=BOTH)
    myscroll.config(command=mytree.yview)
    def callback(event):
        rowid = mytree.identify_row(event.y)
        item = mytree.item(mytree.focus())
        # print(item)
        vals = item.get('values')
        data = f'{vals[0]} : {vals[1]}'
        run_evince(data)
        label.configure(text=data)
        # selection = event.widget.selection()
        # if selection:
        #     index = selection[0]
        #     print(index)
        #     data = event.widget.get(index)
        #     label.configure(text=data)
        #     run_evince(data)
        # else:
        #     label.configure(text='')
    mytree.bind('<<TreeviewSelect>>', callback)

    win.mainloop()



if __name__ == '__main__':
    main()

