import cmd
import shlex
from cowsay import cowsay,cowthink,list_cows,make_bubble

def parseArguments(args):
    words=shlex.split(args)
    message=words[0]
    kwargs={}
    if len(words)>=2: kwargs['cow']=words[1]
    for arg in words[2:]:
        key,value=arg.split('=', 1)
        kwargs[key]=value
    return message, kwargs

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
        
    def do_cowsay(self, args):
        """usage: cowsay <request-message> [<cow-name> {<parameter-name>=<value>}] reply <answer-message> [<cow-name> {<parameter-name>=<value>}]\n\nCreate an image of a talking cow"""
        try:
            message,kwargs=self.parseArguments(args)
            cowthink_message=cowsay(message, **kwargs)
            print(cowthink_message)
        except Exception as e:
            print('An error occurred while executing:',e)
    
    def do_cowthink(self, args):
        """usage: cowsay <request-message> [<cow-name> {<parameter-name>=<value>}] reply <answer-message> [<cow-name> {<parameter-name>=<value>}]\n\nCreate an image of a thinking cow"""
        try:
            message,kwargs=parseArguments(args)
            cowthink_message=cowthink(message, **kwargs)
            print(cowthink_message)
        except Exception as e:
            print('An error occurred while executing:',e)    
    
    def do_EOF(self, args):
        return True

    def postloop(self):
        print("See you soon!")

if __name__=='__main__':
    shell=CowsayShell()
    shell.cmdloop()