source /home/fduvivier/.bash_profile
ssh fduvivier@op5b.local 'echo hi' || echo 'no prob';

screen -S caffeinate -X quit || echo 'no prob';
screen -dmS caffeinate -c 'caffeinate';

SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR
git stash -m "local stuff"

if git pull | grep "Already up to date"
then
    echo "Up to date, not doing anything!"
else
    killall python || echo 'python not running yet';
    killall Python || echo 'Python not running yet';
    poetry install;
    screen -S bot -X quit || echo 'no prob';
    screen -dmS bot bash -c 'source ~/.bash_profile && poetry run python discordbot 2>>log.error.ignorethis.txt 1>>log.ignorethis.txt';
    echo "restarted discordbot"
    ssh fduvivier@192.168.0.55 'echo restarted discordbot' || echo 'no prob';
fi

