# An Implementation of Function-Hiding Inner Product Encryption (FHIPE) #

This is an implementation of the function-hiding inner product encryption scheme 
described here: (link to be posted)

This implementation is a research prototype built for micro-benchmarking 
purposes, and is not intended to be used in production-level code as it has not 
been carefully analyzed for potential security flaws.

Authors:
 * Kevin Lewi, Stanford University
 * Sam Kim, Stanford University
 * Avradip Mandal, Fujitsu Laboratories of America
 * Hart Montgomery, Fujitsu Laboratories of America
 * Arnab Roy, Fujitsu Laboratories of America
 * David J. Wu, Stanford University

Contact Kevin Lewi for questions about the code:
  klewi@cs.stanford.edu

## Prerequisites ##

Make sure you have the following installed:
 * [Python 3.x.x](https://www.python.org/downloads/release/python-350/)
 * [GMP 5.x](http://gmplib.org/)
 * [PBC](http://crypto.stanford.edu/pbc/download.html) 
 * [OpenSSL](http://www.openssl.org/source/)

## Installation ##

    git clone --recursive https://github.com/kevinlewi/fhipe.git
    cd fhipe
    sudo make install (use `make install-mac` if running on MAC OS X)
	
## Running a Test ##

	python3 tests/test_ipe.py

## Modules ##

This library ships with the following modules:
 * **Inner Product Encryption:** In fhipe/ipe.py, implements function-hiding 
   inner product encryption
 * **Two-input Functional Encryption.** In fhipe/mife.py, implements secret-key 
   small-domain two-input functional encryption for arbitrary functions

### Submodules ###

We rely on the following two submodules:
 * [FLINT](http://flintlib.org/) for the C backend 
 * [Charm](http://charm-crypto.com/) for the pairings implementation 


