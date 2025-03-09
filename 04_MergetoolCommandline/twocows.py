import cmd
import shlex
from cowsay import cowsay,cowthink,list_cows,make_bubble

class CowsayShell(cmd.Cmd):
    intro='Welcome to the twocows shell!\nType help or ? for a list of commands\n'
    prompt='twocows> '

    def do_list_cows(self,args):
        """usage: list_cows\n\nList of all available animals"""
        animals=list_cows()
        print('Animals available:')
        for animal in animals:
            print('-', animal)
    
    def do_make_bubble(self, text):
        """usage: make_bubble [<text>]\n\nCreate a speech bubble for text"""
        print(make_bubble(text))
    
    def do_EOF(self, args):
        return True

    def postloop(self):
        print("See you soon!")

if __name__=='__main__':
    shell=CowsayShell()
    shell.cmdloop()