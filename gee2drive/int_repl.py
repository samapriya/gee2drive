import os
import csv
import signal
import sys,time
import pendulum
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.lexers.shell import BatchLexer
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from pygments.styles.tango import TangoStyle
from prompt_toolkit.styles import style_from_pygments
import pkg_resources
import datetime

name=os.name
os.chdir(os.path.dirname(os.path.realpath(__file__)))
src=os.path.dirname(os.path.realpath(__file__))

test_style = style_from_pygments(TangoStyle,{
    Token.Comment:   '#888888 bold',
    Token.Keyword:   '#ff88ff bold',
    Token.Toolbar: '#ffffff bg:#333333',
})
if name=='nt':
    os.system("cls")
elif name=='posix':
    os.system("clear")

ver=pkg_resources.get_distribution("gee2drive").version
l=[]
nm=[]
for items in os.listdir(src):
    if items.endswith('.csv'):
        input_file=csv.DictReader(open(os.path.join(src,items)))
        for rows in input_file:
            l.append(rows['id'])
            nm.append(rows['title'])

CLICompleter=WordCompleter(l,ignore_case=True)
def main():
    def get_bottom_toolbar_tokens(cli):
        now = datetime.datetime.now()
        dt= str(datetime.datetime.now().isoformat()).split('T')[0]
        return [(Token.Toolbar, ' This is Google Earth Engine to Drive Export Manager '+ver+' press Ctrl+C to Exit & cls to Clear Screen. Today is '+dt+'          Current Time:'),
                (Token.Toolbar, '%s:%s:%s' % (now.hour, now.minute, now.second))]
    try:
        while 1:
            inp=prompt(u'> ',
                       history=FileHistory('history.txt'),
                       auto_suggest=AutoSuggestFromHistory(),
                       completer=CLICompleter,
                       get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                       style=test_style,
                       lexer=BatchLexer,complete_while_typing=True,refresh_interval=0.5)
            if inp=="clear":
                if name=='nt':
                    os.system("cls")
                elif name=='posix':
                    os.system("clear")
            elif inp=="exit":
                print("Exiting now")
                time.sleep(1)
                sys.exit()
            else:
                os.system(inp)
    except:
        print ('Goodbye!')

if __name__ == '__main__':
    main()
