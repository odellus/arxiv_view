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
    with open('./config.yaml', 'r') as f:
        return yaml.load(f, yaml.Loader)

def get_arxiv_fpaths(cfg):
    pattern = get_pattern()
    return [
        x for x in os.listdir(cfg['download_dir'])
        if re.match(pattern, x) is not None
    ]

def get_previous():
    with open('./titles.json', 'r') as f:
        return json.load(f)

def persist_result(titles):
    with open('./titles.json', 'w') as f:
        json.dump(titles, f)

def get_arxiv_id(arxiv_fpath):
    return arxiv_fpath[:10]

def get_arxiv_titles(arxiv_fpaths):
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
    persist_result(prev_titles)
    return prev_titles

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
    win.geometry('1200x500')
    mylabel = Label(win, text='Arxiv Titles', font='30')
    mylabel.pack()
    label = Label(win)
    label.pack(side='bottom', fill='x')
    myscroll = Scrollbar(win)
    myscroll.pack(side=RIGHT, fill=Y)
    mylist = Listbox(win, width=800, yscrollcommand=myscroll.set)
    for key, val in titles.items():
        mylist.insert(END, f'{key} : {val}')
    mylist.pack(side=LEFT, fill=BOTH)
    myscroll.config(command=mylist.yview)
    def callback(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            label.configure(text=data)
            run_evince(data)
        else:
            label.configure(text='')
    mylist.bind('<<ListboxSelect>>', callback)

    win.mainloop()



if __name__ == '__main__':
    main()

