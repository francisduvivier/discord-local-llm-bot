source ~/.bash_profile
killall caffeinate || echo 'ok';
caffeinate &;

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
    screen -dmS bot sh -c 'poetry run python discordbot 2>log.error.ignorethis.txt 1>log.ignorethis.txt';
    echo "restarted discordbot"
fi

