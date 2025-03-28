import cmd
import shlex
from cowsay import cowsay,cowthink,list_cows,make_bubble

class CowsayShell(cmd.Cmd):
    intro='Welcome to the twocows shell!\nType help or ? for a list of commands\n'
    prompt='twocows> '
    
    def parseArguments(self, words):
        if len(words)==0: raise ValueError('message is a required argument')
        message=words[0]
        kwargs={}
        if len(words)>=2: kwargs['cow']=words[1]
        for arg in words[2:]:
            key,value=arg.split('=', 1)
            kwargs[key]=value
        return message, kwargs
    
    def alignMessages(self, pictures):
        lines1, lines2=pictures[0].split('\n'), pictures[1].split('\n')
        len1, len2=map(len, [lines1, lines2])
        maxlen1=max(map(len,lines1))
        
        lines1, lines2=[' '*maxlen1]*(len2-len1)+lines1, [' ']*(len1-len2)+lines2
        return '\n'.join([lines1[i]+' '*(maxlen1-len(lines1[i]))+lines2[i] for i in range(max(len1,len2))])
    
    def oneCowProcessing(self, f, words):
        message, kwargs=self.parseArguments(words)
        return f(message,**kwargs)
    
    def twoCowsProcessing(self, f, words):
        index=words.index('reply')
        firstCowWords=words[:index]
        secondCowWords=words[index+1:]
        message1, kwargs1=self.parseArguments(firstCowWords)
        message2, kwargs2=self.parseArguments(secondCowWords)
        pictures=[f(message1,**kwargs1), f(message2,**kwargs2)]
        return self.alignMessages(pictures)
    
    def callHandler(self, f, args):
        words=shlex.split(args)
        t=words.count('reply')
        if t==0:
            return self.oneCowProcessing(f,words)
        elif t==1:
            return self.twoCowsProcessing(f,words)
        else:
            raise ValueError('only one reply is supported')        
    
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
        """usage: cowsay <request-message> [<cow-name> {<parameter-name>=<value>}] [reply <answer-message> [<cow-name> {<parameter-name>=<value>}]]\n\nCreate an image of a talking cow"""
        try:
            print(self.callHandler(cowsay, args))
        except Exception as e:
            print('An error occurred while executing:',e)
    
    def do_cowthink(self, args):
        """usage: cowthink <request-message> [<cow-name> {<parameter-name>=<value>}] [reply <answer-message> [<cow-name> {<parameter-name>=<value>}]]\n\nCreate an image of a thinking cow"""
        try:
            print(self.callHandler(cowthink, args))
        except Exception as e:
            print('An error occurred while executing:',e)   
    
    def do_EOF(self, args):
        return True

    def postloop(self):
        print("See you soon!")

if __name__=='__main__':
    shell=CowsayShell()
    shell.cmdloop()