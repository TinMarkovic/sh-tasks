# SeekandHit tasks

A set of tasks to demonstrate some programming knowledge and experience for SeekandHit.

## Toy Robot

A toy robot written in Python. Readme can be found [here](./sh-toy-robot/).

## Lua & Redis

A lua script to be started in redis is found in `sh-redis-script.lua` to initiate it in a redis instance: 

```bash
# Inside redis, we'd have to assign available parking spaces
: rpush fp 2 4 6 8 10 9 7 5 3 1 11 # etcetera
# Then from command prompt:
redis-cli -h <host> -p <port> -a <secret> --eval sh-redis-script.lua airplane:<number> 
```

## PostgreSQL

SQL code to be executed in a database of your choice is found in `sh-simple-data.sql` with some test data in the code.