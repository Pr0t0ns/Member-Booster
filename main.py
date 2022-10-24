import httpx, random, string, threading, os, json, base64, itertools, time, ctypes, sys

from src.modules.console import console
from src.modules.email import TempMail
from src.modules.discord import Discord
from src.modules.hcaptcha import solve
from src.modules.utils import getRandomFinger
from colorama import init, Fore
from ui import clear

init()

__version__ = "2.1.2"

console.debug("Checking for updates...")
r = httpx.get("https://raw.githubusercontent.com/mciem-better/member-booster/main/version").text.strip("\n")

if r == __version__:
  console.success(f"gen is uptodate!")

console.debug("Updating models list...")
r = httpx.get("https://raw.githubusercontent.com/QIN2DIM/hcaptcha-challenger/main/src/objects.yaml").text

f = open("src\servers\hcap_server\src\objects.yaml", "w", encoding="utf-8")
f.write(r)
f.close()

console.success("Updated models list!", "Starting program...")
time.sleep(3)
os.system("cls")
clear()
class Booster:
  def __init__(self):
    self.start = time.time()
    self.user_file = open('input/names.txt', 'r', encoding='UTF-8')
    self.user_read = self.user_file.read()
    self.usernames = self.user_read.split("\n")
    self.proxies = itertools.cycle(open("input/proxies.txt", "r").read().splitlines())
    self.g, self.u, self.l, self.solved, self.failed_solves, self.average = 0, 0, 0, 0, 0, [1]

    with open('input/config.json') as config_file:
      self.config = json.load(config_file)

  def title(self):
    while True:
      ctypes.windll.kernel32.SetConsoleTitleW(f"G: {self.g} | U: {self.u} | L: {self.l} | S: {self.solved} | FS: {self.failed_solves} | Average solving time: {round(sum(self.average)/len(self.average), 2)}s | Elapsed: {round(time.time() - self.start, 2)}s")
      time.sleep(0.01)

  def gen(self):
    while True:
      try:
        a, b, c = getRandomFinger()
        discord = Discord(a, b, c)

        proxy = next(self.proxies)

        if self.config["use_proxies_with_solver"] == "yes":
          cap, t = solve(proxy=proxy)
        else:
          cap, t = solve(proxy=None)
        self.average.append(t)
        
        if cap == "False":
          continue
        
        self.solved += 1
        console.solved("Solved captcha", cap[:32], str(t) + "s")
        
        if self.config["real_names"] == "no":
          user = self.config["username_prefix"]
          rnd = ('').join(random.choices(string.ascii_letters + string.digits, k=5))
          name = f"{user} | {rnd}"
        else:
          name = random.choice(self.usernames) + ''.join(random.choices(string.ascii_letters + string.digits, k=1))
        
        token = discord.generateToken(cap, proxy, name, self.config["invite"])
        self.g += 1
        console.generated(f"Generated", token[:32])

        '''loc, status_code = discord.checkIfLocked(proxy, token)
        if loc == False:
          console.success("Token Unlocked, checking flags...", token[:32])
          flag = discord.checkFlags(proxy, token)
          self.u += 1
          
          if flag == 0:
            console.success("0 flag", token[:32])
          else:
            console.debug(f"{str(flag)} flag", token[:32])
          
          f = open("output/tokens_unlocked.txt", "a")
          f.write(token + "\n")
          f.close()
        else:
          console.debug("Token Locked", token[:32])
          self.l += 1
          f = open("output/tokens_locked.txt", "a")
          f.write(token + "\n")
          f.close()'''
      except Exception as e:
        if "Server disconnected without sending a response." not in str(e):
           console.error("Error", str(e))

  def main(self):
    am = int(console.input("Threads: "))
    threads = list()
    
    x = threading.Thread(target=self.title)
    threads.append(x)
    x.start()

    for index in range(am):
      x = threading.Thread(target=self.gen)
      threads.append(x)
      x.start()

    for index, thread in enumerate(threads):
      thread.join()

if __name__ == "__main__":
  a = Booster()
  a.main()
