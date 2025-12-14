## Check the running port
lsof -i :8000

## kill using PID 
kill -9 52860

## kill
lsof -ti :8000 | xargs kill -9