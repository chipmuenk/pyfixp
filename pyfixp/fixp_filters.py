import pyfixp.pyfixp as fx
import numpy as np

class Fix_FIR_DF(fx.Fixed):
    """
    Usage:
    Q = Fix_FIR_DF(q_mul, q_acc) # Instantiate fixpoint filter object
    x_bq = self.Q_mul.filt(x, bq)

    The fixpoint object has two different quantizers:
    - q_mul describes requanitization after coefficient multiplication
      ('quant' and 'sat' can both be set to 'none' if there is none)
    - q_acc describes requantization after each summation in the accumulator
            (resp. in the common summation point)

    """
    def __init__(self, q_acc, q_mul = None):
        """
        Initialize fixed object with q_obj
        """
        # test if all passed keys of quantizer object are known
        if q_mul is None:
            q_mul = {'Q':'0.15', 'ovfl':'none', 'quant':'none'}
        self.Q_mul = fx.Fixed(q_mul)
        self.Q_mul.resetN() # reset overflow counter of Q_mul
        self.Q_acc = fx.Fixed(q_acc)
        self.Q_acc.resetN() # reset overflow counter of Q_acc
        self.resetN() # reset filter overflow-counter


    def filt(self, x, bq, verbose = True):
        """
        Calculate FIR filter (direct form) response via difference equation with
        quantization

        Parameters
        ----------
        x : scalar or array-like
            input value(s)

        bq : array-like
            filter coefficients

        Returns
        -------
        yq : ndarray
            The quantized input value(s) as an ndarray with np.float64. If this is
            not what you want, see examples.
        """

        # Initialize vectors (also speeds up calculation)
        yq = accu_q = np.zeros(len(x))
        x_bq = x_mem = np.zeros(len(bq))
        x_mem = np.zeros(len(bq)-1)

        for k in range(len(x) - len(bq)):
            # weighted state-vector x at time k:
            x_bq = self.Q_mul.fixp(np.concatenate([x_mem, x])[k:k + len(bq)] * bq)
            # sum up x_bq to get accu[k]
            accu_q[k] = self.Q_acc.fixp(sum(x_bq))
        yq = accu_q # scaling at the output of the accumulator

        if (self.Q_mul.N_over and verbose): print('Overflows in Multiplier:  ',
                Fixed.Q_mul.N_over)
        if (self.Q_acc.N_over and verbose): print('Overflows in Accumulator: ',
                self.Q_acc.N_over)
        self.N_over = self.Q_mul.N_over + self.Q_acc.N_over

        return yq


# nested loop would be much slower!
#  for k in range(Nx - len(bq)):
#	for i in len(bq):
#	  accu_q[k] = fixed(q_acc, (accu_q[k] + fixed(q_mul, x[k+i]*bq[i+1])))
