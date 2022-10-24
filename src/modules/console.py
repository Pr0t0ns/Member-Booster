from datetime import datetime
from colorama import init, Fore
import threading

init()

lock = threading.RLock() 
class console:
    def success(text1, text2=None):
        date = datetime.now()
        time = datetime.strftime(date, "%H:%M:%S")
        lock.acquire()
        if text2!=None:
            print( Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTGREEN_EX + time+  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTGREEN_EX + "*"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.LIGHTGREEN_EX + text1 + Fore.LIGHTWHITE_EX + " | " + Fore.LIGHTGREEN_EX + text2)
        else:
            print( Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTGREEN_EX + time+  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTGREEN_EX + "*"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.LIGHTGREEN_EX + text1)
        lock.release()

    def debug(text1, text2=None):
          date = datetime.now()
          time = datetime.strftime(date, "%H:%M:%S")
          lock.acquire()
          if text2!=None:
            print( Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTBLUE_EX + time+  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTBLUE_EX + "^"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.LIGHTBLUE_EX + text1 + Fore.LIGHTWHITE_EX + " | " + Fore.LIGHTBLUE_EX + text2)
          else:
            print( Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTBLUE_EX + time+  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTBLUE_EX + "^"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.LIGHTBLUE_EX + text1)

          lock.release()

    def generated(text1, text2):
          date = datetime.now()
          time = datetime.strftime(date, "%H:%M:%S")
          lock.acquire()
          print( Fore.LIGHTWHITE_EX + "[ " +  Fore.CYAN + time+  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.CYAN + "#"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.CYAN + text1 + Fore.LIGHTWHITE_EX + " | " + Fore.CYAN + text2)
          lock.release()

    def solved(text1, text2, text3):
        date = datetime.now()
        time = datetime.strftime(date, "%H:%M:%S")
        lock.acquire()
        print( Fore.LIGHTWHITE_EX + "[ " +  Fore.GREEN + time+  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.GREEN + "$"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.GREEN + text1 + Fore.LIGHTWHITE_EX + " | " + Fore.GREEN + text2 + " | " + Fore.GREEN + text3)
        lock.release()

    def error(text1, text2):
        date = datetime.now()
        time = datetime.strftime(date, "%H:%M:%S")
        lock.acquire()
        print( Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTRED_EX + time +  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTRED_EX + "!"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.LIGHTRED_EX + text1 + Fore.LIGHTWHITE_EX + " | " + Fore.LIGHTRED_EX + text2)
        lock.release()
    
    def input(text):
        date = datetime.now()
        time = datetime.strftime(date, "%H:%M:%S")
        print( Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTYELLOW_EX + time +  Fore.LIGHTWHITE_EX + " ] "+  Fore.LIGHTWHITE_EX + "[ " +  Fore.LIGHTYELLOW_EX + ">"+  Fore.LIGHTWHITE_EX + " ] " +  Fore.LIGHTYELLOW_EX + text, end="")
        return input(Fore.LIGHTWHITE_EX + "")