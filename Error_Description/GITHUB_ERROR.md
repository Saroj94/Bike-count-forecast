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