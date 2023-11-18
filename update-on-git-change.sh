source /home/fduvivier/.bash_profile
SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR
ssh fduvivier@192.168.0.55 "hi there from master"

git stash -m 'local stuff'
git fetch && git checkout todel/keep-bot-alive
