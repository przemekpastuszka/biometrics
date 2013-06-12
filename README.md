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
* Original ![fingerprint](http://github.com/rtshadow/biometrics/tree/master/images/ppf1.png)
* With singular points marked by algorithm: ![poincare](http://github.com/rtshadow/biometrics/tree/master/images/ppf1_poincare.gif)

Note: algorithm marked singular points not only inside fingerprint itself, but on its edges and even outside. This is a result of usage of non-preprocessed image - if the image was enhanced (better contrast, background removed), then only singular points inside fingerprint would be marked.

### Thinning (skeletonization)

How it [works] (http://bme.med.upatras.gr/improc/Morphological%20operators.htm)

Example: ```python thining.py images/ppf1_enhanced.gif --save```

Images:
* ![before](http://github.com/rtshadow/biometrics/tree/master/images/ppf1_enhanced.gif)
* ![after](http://github.com/rtshadow/biometrics/tree/master/images/ppf1_enhanced_thinned.gif)

