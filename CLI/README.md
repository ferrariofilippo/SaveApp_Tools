# SaveApp CLI

A simple command line tool to analyze your SaveApp data.

### Get Started
- Install `python`
- Install `matplotlib`:
```
    python3 -m pip install matplotlib
```
- Set your `.csv` file path:
```
    YOUR_FILE_PATH = 'INSERT PATH TO YOUR FILE HERE'
```
- Set your custom thresholds:
```
    thresholds = [ 10, 50, 200, 1000 ]
```
- You are ready to go!

### CLI Options
Except for `-h`, each option should be preceeded by the list of income tags ids. See the example below:
```
    > python3 ./main.py 1 2 -g
```
- `-s` print statistics
- `-c` create a .csv file containing the net-worth for each month
- `-g` open graph menu
- `-h` show help menu
