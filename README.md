# arxiv_view

A simple way to see what those `2112.83292.pdf` files filling up your Downloads folder are really all about.

## Installation
If for some strange ass reason your linux distro doesn't have evince installed, run `bash install_prereqs.sh` to install it. It is required for viewing the pdfs with a single click.
Create a python virtualenv if you're so motivated. Otherwise you can either say 
```python
python -m pip install PyYaml arxiv
``` 
or 
```python 
python -m pip install -r requirements.txt
```
to get the exact version I am using on my end.  
  

## Configure

Open up `config.yaml` in your favorite text editor/IDE and change it to say
```yaml
download_dir: '/path/to/your/pdfs'
```
You might also want to configure `evince` to fit width by default like so
```bash
gsettings set org.gnome.Evince.Default sizing-mode 'fit-width'
```
## Run  
Open up a terminal and enter
```bash
python arxiv_view.py
```
It can take a while to get all the titles through the `arxiv` package when you're first getting set up, so please be patient.