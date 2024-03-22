@njit(nogil=True, cache=True, fastmath=True, parallel=False)
def AEOT(input_data, auto_avg=3, auto_min=8, auto_max=48, K=0):
    """
    Compute the Autocorrelation Early Onset Trend (AEOT) with autocorrelation Periodogram Algorithm dominant cycle period input.
    """
    
    def nz(value, small_number=1e-10):
        """
        NaN to Zero
        """
        if value == 0 or np.isnan(value):
            return small_number
        return value

    def high_pass_filter_2nd(data, max_len, is_array=False):
        """
        High-pass Filter 2nd order
        """
        trx = 1
        PI = np.pi
        HP = np.zeros_like(data)
        if is_array:
                for i in range(len(data)): 
        
                    angle = 0.707 * trx * PI / max_len[i]
                    alpha = (np.cos(angle) + np.sin(angle) - 1) / np.cos(angle)
                    HP[i] = (1 - alpha / 2) * (1 - alpha / 2) * (nz(data[i]) - 2 *  nz(data[i - 1]) +  nz(data[i - 2])) + 2 * (1 - alpha) *  nz(HP[i - 1]) - (1 - alpha) * (1 - alpha) *  nz(HP[i - 2])

        else:
                for i in range(len(data)): 
                
                    angle = 0.707 * trx * PI / max_len
                    alpha = (np.cos(angle) + np.sin(angle) - 1) / np.cos(angle)
                    HP[i] = (1 - alpha / 2) * (1 - alpha / 2) * (nz(data[i]) - 2 *  nz(data[i - 1]) +  nz(data[i - 2])) + 2 * (1 - alpha) *  nz(HP[i - 1]) - (1 - alpha) * (1 - alpha) *  nz(HP[i - 2])

        return HP
    
    def high_pass_filter(data, max_len, is_array=False):
        """
        High-pass Filter 1st order
        """

        HP = np.zeros_like(data)
        angle = 360 * 3.1415926535897932 / 180
        
        if is_array:

            for i in range(len(data)): 

                alpha = (1 - np.sin(angle / max_len[i])) / np.cos(angle / max_len[i])
                
                HP[i] =  0.5 * (1 + alpha) * (data[i] - nz(data[i - 1])) + alpha * nz(HP[i - 1])

        else:

            alpha = (1 - np.sin(angle / max_len)) / np.cos(angle / max_len)

            for i in range(len(data)): 

                HP[i] =  0.5 * (1 + alpha) * (data[i] - nz(data[i - 1])) + alpha * nz(HP[i - 1])

        return HP

    def super_smoother(data, LPPeriod, is_array=False):
        """
        SuperSmoother Filter
        """

        filtered_data = np.zeros_like(data)
        if is_array:

                for i in range(len(data)):
                    omega = 1.414 * 3.1415926535897932 / LPPeriod[i]
                    a_1 = np.exp(-omega)
                    b_1 = 2 * a_1 * np.cos(1.414 * 3.1415926535897932 / float(LPPeriod[i]))
                    b_2 = b_1
                    a_2 = -a_1 * a_1
                    a_0 = 1 - b_1 - a_2
                    filtered_data[i] = a_0 * (data[i] + nz(data[i - 1])) / 2 + b_1 * nz(filtered_data[i - 1]) + a_2 * nz(filtered_data[i - 2])

        else:

                omega = 1.414 * 3.1415926535897932 / LPPeriod
                a_1 = np.exp(-omega)
                b_1 = 2 * a_1 * np.cos(1.414 * 3.1415926535897932 / float(LPPeriod))
                b_2 = b_1
                a_2 = -a_1 * a_1
                a_0 = 1 - b_1 - a_2

                for i in range(len(data)):
                    filtered_data[i] = a_0 * (data[i] + nz(data[i - 1])) / 2 + b_1 * nz(filtered_data[i - 1]) + a_2 * nz(filtered_data[i - 2])


        return filtered_data

    def _auto_dom_imp(src, min_len, max_len, ave_len):

        high_pass = high_pass_filter(src, max_len, False)
        filt = super_smoother(high_pass, min_len, False)

        dominant_cycles = np.full(len(src), 1)
        arr_size = max_len * 2

        r = np.zeros(shape=(len(src), max_len+1))

        for i in range(max_len, len(src)):

            corr = np.zeros(max_len+1)
            cospart = np.zeros(max_len+1)
            sinpart = np.zeros(max_len+1)
            sqsum = np.zeros(max_len+1)

            pwr = np.zeros(arr_size)

            # Pearson correlation for each value of lag
            for lag in range(0, max_len+1):

                m = ave_len if ave_len > 0 else lag
                Sx, Sy, Sxx, Syy, Sxy = 0.0, 0.0, 0.0, 0.0, 0.0

                for mi in range(0, m):

                    x = nz(filt[i - mi])
                    y = nz(filt[i - (lag + mi)])

                    Sx += x
                    Sy += y
                    Sxx += x * x
                    Sxy += x * y
                    Syy += y * y

                    denom = (m * Sxx - Sx * Sx) * (m * Syy - Sy * Sy)

                if denom > 0:
                    corr[lag] = (m * Sxy - Sx * Sy) / np.sqrt(denom)

            # Power spectrum density calculation
            # Discrete Fourier transform
            # Correlate autocorrection values with the cosine and sine of each period of interest
            # The sum of the squares of each value represents relative power at each period
            maxpwr = 0.0
            for period in range(min_len, max_len+1):

                cospart[period] = sinpart[period] = 0.0

                for n in range(ave_len, max_len+1):

                    cospart[period] += nz(corr[n]) * np.cos(6.28318 * n / period)
                    sinpart[period] += nz(corr[n]) * np.sin(6.28318 * n / period)

                sqsum[period] = nz(cospart[period]**2) + nz(sinpart[period]**2)
                r[i][period] = 0.2 * nz(sqsum[period]**2) + 0.8 * nz(r[i-1][period])

                if nz(r[i][period]) > maxpwr:
                    maxpwr = nz(r[i][period])

            # Set the power array values up to max_len normalized by maxpwr, handling NaN with np.nan_to_num
            for period in range(ave_len, max_len + 1):  # assuming ave_len <= max_len
                pwr[period] = (nz(r[i][period]) / nz(maxpwr))

            # Initialize peak power to zero
            spx, sp, peakpwr, dominant_cycle = 0.0, 0.0, 0.0, 0.0
            # Loop through pwr for elements min_len to max_len to find the peak power
            for period in range(min_len, max_len + 1):

                pwr_value = nz(pwr[period])

                if pwr_value > peakpwr:
                    peakpwr = pwr_value

                if pwr_value >= 0.5:
                    spx += period * pwr_value
                    sp += pwr_value

                if peakpwr >= 0.25 and pwr_value >= 0.25:
                    spx += period * pwr_value
                    sp += pwr_value

            dominant_cycle = (spx / sp) if sp != 0 else dominant_cycles[i-1] if sp < 0.25 else dominant_cycle

            # Ensure dominant_cycle is at least minimum length
            dominant_cycle = max(dominant_cycle, min_len)

            dominant_cycles[i] = dominant_cycle

        return dominant_cycles


    def agc(data):
        """
        Fast Attack - Slow Decay Algorithm
        """
        X = np.zeros_like(data)
        Peak = np.zeros_like(data)

        for i in range(len(data)):
            if i == 0:
                X[i] = data[i]
                Peak[i] = abs(data[i])
            else:
                Peak[i] = 0.991 * Peak[i - 1]
                if abs(data[i]) > Peak[i]:
                    Peak[i] = abs(data[i])
                if Peak[i] != 0:
                    X[i] = data[i] / Peak[i]
                else:
                    X[i] = 0

        return X
    
    def quotient(data, K_val):
        """
        Calculate the quotient using input data and K value.
        """
        K = K_val
        Q = np.zeros_like(data)
        for i in range(len(data)):
            if i <= 1:
                Q[i] = 0
            else:
                Q[i] = (data[i] + K) / (K * data[i] + 1)
        return Q
    
    dominant_cycles = _auto_dom_imp(input_data, auto_min, auto_max, auto_avg)

    HP = high_pass_filter(input_data, dominant_cycles, True)

    Filt = super_smoother(HP, dominant_cycles, True)

    X = agc(Filt)
    
    Q = quotient(X, K)

    return Q, dominant_cycles
