import sys
import Leap
from Leap import SwipeGesture
import platform
import time
import os


operatingsystem = platform.system()
if operatingsystem == "Darwin":
    import subprocess

    def lock_screen_darwin():
        subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend', shell=True)

    def spawn_app_darwin():
        print "Spawning of applications not yet supported on Darwin"

    lock_screen = lock_screen_darwin
    spawn_app = spawn_app_darwin

elif operatingsystem == "Windows":
    import ctypes

    def lock_screen_windows():
        ctypes.windll.user32.LockWorkStation()

    def spawn_app_windows():
        olddir = os.path.dirname(os.path.realpath(__file__))
        os.chdir("C:/Program Files (x86)/Google/Chrome/Application/")
        os.system("chrome.exe --new-window http://reddit.com/r/netsec")
        os.chdir(olddir)

    lock_screen = lock_screen_windows
    spawn_app = spawn_app_windows
else:
    print "Unsupported System: %s" % operatingsystem
    sys.exit(1)


class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                lock_screen()
                print "locking screen"
                time.sleep(5)
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = SwipeGesture(gesture)
                spawn_app()
                print "spawn chrome"
                time.sleep(5)


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    controller.config.set("Gesture.Swipe.MinLength", 50.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 10)
    controller.config.save()

    print "Running on %s" % platform.system()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()