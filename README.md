# About
**If you are insterested in QPython running on Android, visit the [android](https://github.com/cleardusk/UCAS/tree/android) branch.**

This is a very simple tool to auto-login on campus network, you can also write it if you know a little about `request`
library.

More features will be added if time and energy permits.

# Usage
Now the script support UCAS/Wireless and ChinaUnicom!
## UCAS
First, you should add your id and password in config.json, the id is your student number, the initial password is the last six 
characters of your personal ID card number. And follows

```
# login
python ucas.py
# or
python ucas.py -D login
# or the complete command: D is action, C is config, O is option
python ucas.py -D login -C config.json -O ucas

# logout
python ucas.py -D logout
```

## ChinaUnicom
Similar to UCAS, user id is your phone number, and the password is six digit number initially
```
# login, complte command
python ucas.oy -D on -C config.json -O cu
# shortest command
python ucas.py -O cu

# logout, shortest command
python ucas.py -D logout -O cu
```

You can change or simplify the command if you spend a little time to dive into the code.

I wrote it using Python 2.x, but the code works in Python 3.x too.

# More
If the code helps you in any way, please share it with more people who need. You can also star to support me~

Welcome to contact me about things in Python, coding and so on...

## Linux
If you are using the linux distribution based on Ubuntu, a convenient method to auto connect specific wifi follows:
```
nmcli c
nmcli c up uuid <paste uuid here>
```

I work on Mint, my login pipline is like this
```
nmcli c up uuid a0df920b-9ad2-460a-b690-5163d9b2b099 && ucas.py -D login
```