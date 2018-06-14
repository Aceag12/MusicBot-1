#/bin/bash
#------------------------------------------------------------
#
# GNU Screen bash startup script (Linux only)
#
# This script is intended to start the Discord MusicBot. A couple
# assumptions are made regarding its setup:
# 1. MusicBot was built and configured to run within a venv
# 2. Screen is installed and working properly, and its usage is
#    not foreign to you.
#
# When run, the script will check for existing screen sessions of the
# same Screen name (e.g. MusicBot). If the MusicBot screen already
# exists, it will be simply re-attached.
#
# Otherwise it will be created and screenrun.sh will be re-invoked
# within the screen session, where the venv will be activated and
# MusicBot will be started.
#
# Usage:
#
# 1. First make sure MusicBot can be started manually.
# 2. Edit the GAMENAME, VIRTUALENV and GAMEDIR vars below to
#    match your game.
# 3. Make it executable with 'chmod u+x screenrun.sh'.
#
#------------------------------------------------------------

# CHANGE to fit your game (obs: no spaces around the '=')

GAMENAME="MusicBot"
VIRTUALENV="/home/daniel/Discord3_6"
GAMEDIR="/home/daniel/Discord3_6/MusicBot"

#------------------------------------------------------------

if [ -z "$STY" ]; then
	if screen -S "$GAMENAME" -X select .>/dev/null; then
		# Session already exists. Send the start command instead.
		echo "Discord MusicBot is already running. Reattaching..."
		cd "$GAMEDIR"
		screen -r "$GAMENAME"
	else
		# start GNU Screen then run it with this same script, making sure to
		# not start Screen on the second call
		echo "Starting Discord MusicBot."
		exec screen -d -m -S "$GAMENAME" -t evennia /bin/bash "$0" "$1"
	fi
else
	# Screen socket is non-zero. Execute in the GNU Screen session.
	source "$VIRTUALENV"/bin/activate
	cd "$GAMEDIR"
	# start evennia itself
	python run.py
	# we must run this to avoid the screen session exiting immediately
	exec sh
fi

