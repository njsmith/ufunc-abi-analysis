#!/usr/bin/env python

import glob
from codetrawl.report import make_report, group, filter

junk = [group("NumPy itself",
              [filter("path", r"/ufuncobject\.h$"),
               filter("path", "/numpy/core"),
               filter("path", "/numpy/lib"),
               filter("path", "/numpy/f2py"),
               filter("path", "/numpy/linalg"),
               filter("path", r"/__ufunc_api\.h"),
              ]),
        group("NumPy forks / precursors / etc.",
              [filter("repo", "bohrium/numpy", "numpy fork"),
               filter("repo", "wolfgarnet/numpycbe", "numpy fork"),
               filter("repo", "teoliphant/numpy-refactor",
                      "defunct attempt to refactor numpy"),
               filter("path", "/Numeric-", "Numeric"),
               filter("path", r"/Src/ufuncobject\.c", "Numeric"),
               filter("path", r"/Src/arrayobject\.c", "Numeric"),
              ]),
        group("Redundant",
              [filter("path", "/site-packages/",
                      "someone checked in their venv/conda tree; "
                      "we'll find the upstream project elsewhere"),
              ]),
        ]

make_report("PyUFuncObject", glob.glob("pyufuncobject/*PyUFuncObject*"),
            "pyufuncobject-report.html",
            junk + [
                group("Cython-generated boilerplate",
                      [filter("line",
                              r"_Pyx_ImportType.*sizeof\(PyUFuncObject\)"),
                      ]),
                group("Numba -- audited, REAL",
                      [filter("repo", "[Nn]umba")]),
                group("dynd-python -- audited, REAL",
                      [filter("repo", "dynd-python")]),
                group("gulinalg -- audited, only unused debugging code affected",
                      [filter("repo", "ContinuumIO/gulinalg")]),
                group("rational dtype code -- audited, uses ufunc->nargs only",
                      [filter("line", r"PyUFuncObject\* ufunc =")]),
            ])

# Trying to catch all of:
#   cdef ufunc f
#   cdef XX.ufunc f
#   <ufunc> f
#   <XX.ufunc> f
#   cdef foo(ufunc f):
#   cdef foo(XX.ufunc f):
make_report(r"(cdef\W+(|.*\.\W*)ufunc)|(<.*ufunc\W*>)|(cdef.*\(.*ufunc)",
            glob.glob("pyufuncobject/*-ufunc-cython.gz"),
            "ufunc-cython-report.html",
            junk + [
            ])
