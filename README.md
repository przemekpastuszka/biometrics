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

How it works:
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
