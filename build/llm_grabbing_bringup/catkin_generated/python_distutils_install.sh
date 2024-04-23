#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ros/ur5_sim/src/llm_grabbing_bringup"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ros/ur5_sim/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ros/ur5_sim/install/lib/python3/dist-packages:/home/ros/ur5_sim/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ros/ur5_sim/build" \
    "/usr/bin/python3" \
    "/home/ros/ur5_sim/src/llm_grabbing_bringup/setup.py" \
     \
    build --build-base "/home/ros/ur5_sim/build/llm_grabbing_bringup" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ros/ur5_sim/install" --install-scripts="/home/ros/ur5_sim/install/bin"
