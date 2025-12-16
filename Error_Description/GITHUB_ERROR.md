To https://github.com/Saroj94/Bike-count-forecast.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/Saroj94/Bike-count-forecast.git'
hint: Updates were rejected because a pushed branch tip is behind its remote
hint: counterpart. If you want to integrate the remote changes, use 'git pull'
hint: before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

## solution
1. git pull --rebase origin main
2. git add .
3. git rebase --continue
4. git push origin main
## Best Practice
1. git pull --rebase
2. git push

## Github error
! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/Saroj94/Bike-Rental-forecasting.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

**Solution**
! [rejected]        main -> main (non-fast-forward)
1. git pull origin main --rebase
2. git push origin main

## Error
- sarojs-MacBook-Air:Bike-count-forecast sarojrai$ git pull 
error: Pulling is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.

# 1. Resolve the conflict by confirming the deletion
git rm notebook/Bike_Rental_EDA.ipynb

# 2. Continue the rebase process
git rebase --continue

# 3. Once the rebase is complete and you are back on the main branch,
#    you can check the status and then force push (if the rebase rewrote history)
#    *Only use --force if you know your rebase rewrote history and you are on a branch
#    only you are working on.*
# git status 
# git push origin main --force