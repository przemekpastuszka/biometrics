# Fingerprint recognition algorithms

Active development year: 2012

## Summary
Some implementations of fingerprint recognition algorithms developed for Biometric Methods course at University of Wrocław, Poland.

## Usage

### Prerequisites
* python 2.7
* python imaging library (PIL)

### How to use it
Simply do ```python filename.py --help``` to figure out how to execute ```filename``` algorithm

## Algorithms

### Poincaré Index
Finds singular points on fingerprint. 

How it works (more detailed description [here](http://books.google.pl/books?id=1Wpx25D8qOwC&lpg=PA120&ots=9wRY0Rosb7&dq=poincare%20index%20fingerprint&hl=pl&pg=PA120#v=onepage&q=poincare%20index%20fingerprint&f=false)):
* divide image into blocks of ```block_size```
* for each block: 
    * calculate orientation of the fingerprint ridge in that block (i.e. what is the rigde slope / angle between a ridge and horizon)
    * sum up the differences of angles (orientations) of the surrounding blocks
    * there are 4 cases:
        * sum is 180 (+- tolerance) - loop found
        * sum is -180 (+- tolerance) - delta found
        * sum is 360 (+- tolerance) - whorl found

The python script will mark the singularities with circles:
* red for loop
* green for delta
* blue for whorl
      
Example: ```python poincare.py images/ppf1.png 16 1 --smooth```

Images:
* Original 

![fingerprint](https://raw.github.com/rtshadow/biometrics/master/images/ppf1.png)

* With singular points marked by algorithm: 

![poincare](https://raw.github.com/rtshadow/biometrics/master/images/ppf1_poincare.gif)

Note: algorithm marked singular points not only inside fingerprint itself, but on its edges and even outside. This is a result of usage of non-preprocessed image - if the image was enhanced (better contrast, background removed), then only singular points inside fingerprint would be marked.

### Thinning (skeletonization)

How it [works] (http://bme.med.upatras.gr/improc/Morphological%20operators.htm#Thining)

Example: ```python thining.py images/ppf1_enhanced.gif --save```

Images:
* Before

![before](https://raw.github.com/rtshadow/biometrics/master/images/ppf1_enhanced.gif)

* After:

![after](https://raw.github.com/rtshadow/biometrics/master/images/ppf1_enhanced_thinned.gif)

### Minutiae recognition (crossing number method)
Crossing number methods is a really simple way to detect ridge endings and ridge bifurcations.

First, you'll need thinned (skeleton) image (refer to previous section how to get it). Then the crossing number algorithm will look at 3x3 pixel blocks:
* if middle pixel is black (represents ridge):
    * if pixel on boundary are crossed with the ridge once, then we've found ridge ending
    * if pixel on boundary are crossed with the ridge three times, then we've found ridge bifurcation
    
Example: ```python crossing_number.py images/ppf1_enhanced_thinned.gif --save```

![minutiae](https://raw.github.com/rtshadow/biometrics/master/images/ppf1_enhanced_thinned_minutiae.gif)
