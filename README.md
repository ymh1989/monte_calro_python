## Monte Carlo simulation using Python

### Introduction

Here is an implementation of Monte Carlo simulation(MCS) for pricing derivatives using Python. Not only general method for MCS but also vectorization codes are tested.

The main purpose is to introduce the MCS for finance. All of programs in this repe are performed by Python.

### Methods

As I mentioned in `Vectorization` repo, the main reason for performance of MCS is `loop`. Here, I tested the `Numpy` which is library for linear algebra in Python. Detailed information of `Numpy` can be found in [Numpy-Python](www.numpy.org/).

### Environment

- CPU : Intel(R) Core(TM) i5-6400 @ 2.7GHZ
- RAM : DDR3L 16GB PC3-12800
- [Python 2.7](https://www.python.org/), [numpy 1.10.4](http://www.numpy.org/)

### Result

- In this repo, I compare the performance between CPU and GPU. The parameters can be modified freely.

|            | European call         | Up&out call           | ELS 1-asset (Price)    | ELS 2-asset (Price)    | ELS 3-asset (Price)    |
|------------|-----------------------|-----------------------|------------------------|------------------------|------------------------|
| General MCS | 1.2341s <p>(10<sup>6</sup> simuls)</p> | 1.7619s <p>(10<sup>5</sup> simuls)</p>                   | 11.0568s <p>(10<sup>4</sup> simuls)</p> | 45.4266s <p>(10<sup>4</sup> simuls)</p> | 68.9585s <p>(10<sup>4</sup> simuls)</p> |
| Vec MCS | 0.0785s <p>(10<sup>6</sup> simuls)</p> | N/A | 0.6229s <p>(10<sup>4</sup> simuls)</p>  | 1.4709s <p>(10<sup>4</sup> simuls)</p>  | 2.2230s <p>(10<sup>4</sup> simuls)</p>  |

### Note
- If you're interested in my works, please [email](mailto:yoomh1989@gmail.com) me.