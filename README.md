# ares_to_moog

This codes reads the output of [ARES](http://www.astro.up.pt/~sousasag/ares/)
and transforms it into [MOOG](http://www.as.utexas.edu/~chris/moog.html)
readable format.

To run this code, you need a file with the line list & atomic data -->
`make_linelist.dat` and type:

    python make_linelist.py

As an example, I include the line list file (`make_linelist.dat`) and an ARES
output (`star.ares`). To make the process automatic, put the `*.ares` into an
auxiliary file (`makelines`).

    ls -1 *.ares > makelines

