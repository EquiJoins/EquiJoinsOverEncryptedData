# Search Over Encrypted Data

This is an implementation of an algorithm to search over encrypted data.
Specifically, given two tables `A` and `B`, some join attributes `A.a` and `B.b`,
and a filter clause `A.x = c_a and B.y = c_b`, we would like to perform the following query
```sql
SELECT * FROM A
INNER JOIN B ON A.x = B.x
WHERE A.a IN (s_1) AND B.b IN (t_1)
```
(for constants `s_1`, `t_1`), with minimal leakage. That is, using a (master) secret key, 
we would like to encrypt the tables (i.e. their rows),
execute an encrypted query on them, resulting in the retrieval of the correct rows.

See [this paper](http://www.fkerschbaum.org/icde19.pdf) for a formal description
of the algorithm implemented in this repository.

This implementation uses a
[function-hiding inner product encryption scheme](https://eprint.iacr.org/2016/440.pdf)
whose code is contained in [fhipe](fhipe). Section 2.3 of the paper is the API specification
for the functionality implemented in [fhipe/ipe.py](fhipe/ipe.py).
See the [fhipe project's readme](https://github.com/kevinlewi/fhipe) for more details.

## Prerequisites ##

Make sure you have the following installed:
 * [Python 3.x.x](https://www.python.org/downloads/release/python-350/)
 * [GMP 5.x](http://gmplib.org/)
 * [PBC](http://crypto.stanford.edu/pbc/download.html) 
 * [OpenSSL](http://www.openssl.org/source/)

## Installation ##

```bash
 $ git clone --recursive https://git.uwaterloo.ca/fkerschb/encrypted-joins.git
 $ cd encryped-joins
 $ sudo make install # ( or use `make install-mac` if running on MAC OS X)
```

### Build Errors and How to Fix Them ###
See the following list for common build errors and how to fix them.
1. **Error**: `charm/core/math/integer/integermodule.c:129:19: error: dereferencing pointer to incomplete type ‘BIGNUM {aka struct bignum_st}’`
 
   **Resolution**: this is a [known issue](https://github.com/JHUISI/charm/issues/135) with an older version of `charm`. 
   Using the latest dev branch of the `charm` repo should resolve this (i.e. `cd charm` and `git checkout dev`).

## Running Experiments ##
In [hash_based_join.py](hash_based_impl/hash_based_join.py), we run a hash based join
on TPC-H data (schema found [here](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf#page=13])). 
In the `hash_based_impl/data/` folder, one can find the datasets separated by the scale factor used to generate them.
We only use the `orders` table and `customer` table. For these tables, we have appended a column `selectivity`
to have granular control over which rows are selected in a `WHERE` clause. For example, for selectivity `1/100`,
there will be `num_rows / 100` rows that have value `100` for the `selectivity` attribute.

## Notes from Previous Development ##

The organization of the py submodules are as follows
 * [fhipe/ipe.py](fhipe/ipe.py) contains the code required to generate the vectors, ciphertext and tag
 * [fhipe/join.py](fhipe/join.py) contains the code to run the actual join query - currently it is a nested inner loop join
 * [fhipe/encrypt_functions.py](fhipe/encrypt_functions.py) contains the code required to encrypt a specific row or table - typically done as a preprocessing step

Typical workflow
 * Load in a table from a csv file to a 2d array
 * Determine the number of attributes that are in the query, the vector length is equal to the number of
 attributes plus 4
 * Generate a secret key by calling ipe.setup(int) and passing in the vector length
 
