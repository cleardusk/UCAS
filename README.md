# About
This is a very simple tool to auto-login on campus network, you can also write it if you know a little about `request`
library.

More features will be added if time and energy permits.

# Usage
First, you should add your id and password in config.json, the id is your student number, the password is the last six 
character of your personal ID card number.

```
# login
python ucas.py
# or
python ucas.py -D login

# logout
python ucas.py -D logout
```

I wrote it using Python 2.x, but the code works in Python 3.x too.

# More
Welcome for more contributors...

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