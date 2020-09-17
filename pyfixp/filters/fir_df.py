import pyfixp.pyfixp as fx
import numpy as np

class FIR_DF(fx.Fixed):
    """
    Usage:
    Q = FIR_DF(b, q_mul, q_acc) # Instantiate fixpoint filter object
    x_bq = self.Q_mul.filt(x, bq)

    The fixpoint object has two different quantizers:
    - b is an array with coefficients
    - q_mul describes requanitization after coefficient multiplication
      ('quant' and 'sat' can both be set to 'none' if there is none)
    - q_acc describes requantization after each summation in the accumulator
            (resp. in the common summation point)

    """
    def __init__(self, b, q_acc, q_mul = None, zi = None):
        """
        Initialize fixed object with q_obj
        
        Parameters
        ----------

        b : array-like
            filter coefficients
            
        q_acc : dict
                dictionary with quantizer settings for the accumulator
                
        q_mul : dict
                dictionary with quantizer settings for the partial products (optional)
                
        zi : array-like
            past values of filter input for filter initialization; maximum length is 
            len(b) - 1. The rest is filled with zeros, when zi is None, the 
        """
        # test if all passed keys of quantizer object are known
        if q_mul is None:
            q_mul = {'Q':'0.15', 'ovfl':'none', 'quant':'none'}
        self.Q_mul = fx.Fixed(q_mul) # create quantizer for partial product
        self.Q_acc = fx.Fixed(q_acc) # create quantizer for accumulator
        self.b = b # coefficients
        self.N = len(self.b) - 1 # filter order
        
        self.init(zi)


    def init(self, zi=None):
        """
        Initialize filter by resetting all counters

        Parameters
        ----------
        zi : array-like
            initialize filter memory

        Returns
        -------
        None.

        """
        self.Q_mul.resetN() # reset overflow counter of Q_mul
        self.Q_acc.resetN() # reset overflow counter of Q_acc
        self.N_over_filt = 0 # total number of overflows in filter
        
        # Initialize vectors (also speeds up calculation)
        self.xbq = np.zeros(len(self.b)) # partial products
        
        if zi is None:
            self.xi = np.zeros(self.N)
        else: # initialize filter memory and fill up with zeros
            if len(zi) == self.N - 1:
                self.xi = zi
            elif len(zi) < self.N:
                self.xi = np.concatenate((zi, np.zeros(self.N - len(zi))))
            else:
                self.xi = zi[:self.N]

        
    def update(self, b):
        """
        Load filter with new set of coefficients
        
        Parameters
        ----------

        b : array-like
            filter coefficients. Length must be identical to the coefficient
            set used during initialization
            
        Returns
        -------
        
        nothing
            
        """
        if len(b) == len(self.b):
            self.b = b
        else:
            raise IndexError("Number of coefficients differs from initialization!")
        return
        
        

    def fxfilter(self, b, x, zi=None):
        """
        Calculate FIR filter (direct form) response via difference equation with
        quantization

        Parameters
        ----------
        x :  scalar or array-like
             input value(s)

        b :  array-like
             filter coefficients; when None, the old coefficients are left untouched
            
        zi : array-like
             initial conditions; you can 
            

        Returns
        -------
        yq : ndarray
            The quantized input value(s) as a scalar or an ndarray with np.float64.
            and the same shape as x.
        """
        
        if b is not None: # update coefficients
            if len(b) == len(self.b):
                self.b = b
            else:
                raise IndexError("Number of coefficients differs from initialization!")
            
        if zi is not None: # initialize filter memory and fill up with zeros
            if len(zi) == len(b) - 1:
                self.xi = zi
            elif len(zi) < len(b) - 1:
                self.xi = np.concatenate((zi, np.zeros(len(self.b - 1 - len(zi)))))
            else:
                self.xi = zi[:len(b)]


        yq = np.zeros(len(x))
        for k in range(len(x) - len(self.b)):
            # weighted state-vector x at time k:
            self.xbq = self.Q_mul.fixp(np.concatenate((self.xi, x))[k:k + len(self.b)] * self.b)
            # sum up x_bq to get accu[k]
            yq[k] = self.Q_acc.fixp(np.sum(self.xbq))
        self.xi = np.concatenate((self.xi, x))[-self.N:] # store last N inputs
        self.N_over_filt = self.Q_acc.N_over + self.Q_mul.N_over

        return yq


# nested loop would be much slower!
#  for k in range(Nx - len(bq)):
#	for i in len(bq):
#	  accu_q[k] = fixed(q_acc, (accu_q[k] + fixed(q_mul, x[k+i]*bq[i+1])))
