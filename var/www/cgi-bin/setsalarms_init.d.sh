#! /bin/sh
### BEGIN INIT INFO
# Provides:          setsalarms_d.py
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Run setsalarms_d.py if it exist
### END INIT INFO

DIR=/var/www/cgi-bin
DAEMON=$DIR/setsalarms_d.py
DAEMON_NAME=setsalarms_d

# Add any command line options for your daemon here
DAEMON_OPTS=$2

# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=www-data

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/init/vars.sh
. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    ($DAEMON $DAEMON_OPTS &) &
    log_end_msg $?
}

do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    PID=`ps -e -o pid,cmd | grep "$DAEMON_NAME[.]py $DAEMON_OPTS" | awk '{ print $1 }'`
	echo $PID
	if [ "$PID" != "" ]
		then
			kill $PID
		else
			echo "$DAEMON_NAME not running ?"
	fi
    log_end_msg $?
}

# Controllo il numero dei parametri passati da linea di comando!
# Questo script e` diverso dal solito, necessita di un parametro
# per avviare il suo 'sottoprogramma', piu` che altro, non posso
# esguire uno stop "a caso", devo fermarne uno specifico, non il
# primo pid che trova.
if [ "$#" != "2" ]
	then
		echo "Il numero dei parametri non e\` corretto"
		exit 2
fi

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
		PID=`ps -e -o pid,cmd | grep "$DAEMON_NAME[.]py $DAEMON_OPTS" | awk '{ print $1 }'`
		if [ "$PID" != "" ]
		  then
			echo "$DAEMON_NAME is running!"
			echo "Pid is: $PID"
		  else
			echo "$DAEMON_NAME not running!"
		fi
        exit $?
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
