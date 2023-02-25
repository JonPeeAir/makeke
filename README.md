# makeke
A script that helps me generate makefiles for my C++ projects

## Usage
Run makeke.py inside the root directory of the C++ project passing to it your main file as an argument 

ex.  
```
[path to makeke.py]/makeke.py main.cpp
```

## Tip
To avoid having to type the whole `[path to makeke.py]/makeke.py`, create a symbolic link to makeke.py inside one of the directories defined in $PATH  

Here's how I would do it

Create a /bin directory inside your $HOME directory
```
mkdir ~/bin
```

Open your .bashrc and add this line of code at the end of the file
```
export PATH="$HOME/bin:$PATH"
```

Now you either restart your terminal or run this command
```
source ~/.bashrc
```

Now that $HOME/bin has been added to $PATH, Create the symbolic link inside $HOME/bin
```
ln -s [path to makeke.py]/makeke.py ~/bin/makeke
```

Running `which makeke` should now show the location of your symbolic link as `/home/[usr name]/bin/makeke`

You can now use the script like so
```
makeke main.cpp
```
