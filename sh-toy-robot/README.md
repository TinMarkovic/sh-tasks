# SeekandHit Toy Robot

A toy robot written in Python. 

## Requirements

Python 2.7

To install requirements, you'd have to run `pip install -r requirements.pip.txt` or alternatively just `pip install enum34`. The requirement lies with the cross-compability Python library for enumerations (innate in some installations) and is there for compatibility. 

## Execution

To execute the robot for arbitrary commands, you can do so over the command line interface:

```bash
python shtoyrobot.py 'PLACE 0,0,NORTH MOVE REPORT' 
python shtoyrobot.py 'PLACE 0,0,NORTH LEFT REPORT' 'PLACE 1,2,EAST MOVE MOVE LEFT MOVE REPORT'
```

Each argument to the command will be executed, so multiple commands can be executed at once - their results show.

## Tests

To run tests of the script, simply do `python shtests.py`.