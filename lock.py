import sys
import Leap
from Leap import SwipeGesture
import ctypes


class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']


    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        for gesture in frame.gestures():
            for hand in frame.hands:
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    ctypes.windll.user32.LockWorkStation()
                    print "locking screen"
                    #print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                    #        gesture.id, self.state_names[gesture.state],
                    #        swipe.position, swipe.direction, swipe.speed)




def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    controller.config.set("Gesture.Swipe.MinLength", 50.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 10)
    controller.config.save()

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