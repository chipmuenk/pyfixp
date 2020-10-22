# pyfixp
A Python library for fast fixpoint arithmetics based on `numpy`.

This library was originally created for the Python Filter Design and Analysis 
[pyFDA](https://github.org/chipmuenk/pyfda) project but can also be used standalone.

Most routines operate on scalars and arrays alike, currently the following operations are supported:

- (Re)Quantization ('floor', 'round', 'fix') with two's complement wrap around ('wrap') 
  or saturation behaviour ('sat' ) 
- Conversion of binary, hex, decimal, CSD format strings to float and vice versa

![Screenshot](img/pyfixp_screenshot.png)

(Re-)quantizers read and write numpy scalars and arrays,
allowing easy interfacing to e. g. float stimuli and matplotlib plotting. 
Fixpoint and format conversion behaviour and the number of integer 
and fractional bits is controlled with dictionaries. 

## Example
In the following example a quantizer 
is defined with an output format of 0 integer bits and 3 fractional bits, 
overflows are wrapped around in two's complement style ("wrap") and additional 
fractional bits are simply truncated ("floor"):

    import pyfixp as fx
    q_dict = {'WI':0, 'WF': 3,               # number of integer / fractional bits
          'quant':'floor', 'ovfl': 'wrap'}   # quantization / overflow behaviour
    Q = fx.Fixed(q_dict)                     # instance of fixpoint class Fixed()
    for i in np.arange(12)/10:               # i = 0, 0.1, 0.2, ...
        print("q<{0:>3.2f}> = {1:>5.3f}".format(i, Q.fixp(i))) # quantize i

The options are shown by entering `fx.Fixed?` in the notebook.

More examples can be found in the `doc` subdirectory containing a.o. the Jupyter notebooks

- [intro_pyfixp.ipynb: ](doc/intro_pyfixp.ipynb) An introduction to using pyfixp for quantizing and saturating signals
- [fixpoint_filters.ipynb: ](doc/fixpoint_filters.ipynb) An introduction to fixpoint filters and how to implement them with pyfixp


