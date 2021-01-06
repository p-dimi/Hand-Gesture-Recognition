# Hand-Gesture-Recognition
Light and easy hand gesture recognition script, specifically made for controlling grid-based buttons (or other things which are on a grid).

![HandGesture](demo.gif)

The concept is this:

Suppose you have several buttons you want to be able to control with hand gestures.
The buttons are divided on an NxN grid, such as a 3x3 grid (the default grid size).

Running the script will read from your camera feed, and will detect when you are changing your hand gesture from an open palm to a fist.
Changing the gesture will activate the button.
The location of the hand when the gesture is changed is registered as well.

You will need to modify this code for your own needs if you actually want to use it.

Note: Only when changing from open to closed, is it registered as activated. Continuing to hold a closed palm will not register as activated.
You can change that in the code if you'd like. I personally wanted only the moment of gesture change to register.

### How it works:
Run hand_detect.py

You will see in the console that it is constantly printing a status (False / True) and a position (X, Y) on a  grid.

You will also see on the video display that there is a colored circle around your hand, green for closed fist, red for open palm.

The status of whether you changed your hand from open to closed palm is stored in the variable:
<b>select</b>

The location of the hand is stored in the variable:
<b>pos</b>

To make use of the code, simply make use of these two variables.

Do whatever you want with it, implement it in whichever project you'd like, etc.

### Changing settings:
You can change settings in the code by editing the code and altering the variables under the "## SETTINGS ##" segment.
