# Early Onset Trend (EOT) Indicator

The Early Onset Trend (EOT) indicator is a technical analysis tool used to detect the onset of trends in financial time series data. It combines several signal processing techniques, including autocorrelation, high-pass filtering, and adaptive gain control (AGC), to identify the dominant cycle period and extract the underlying trend from the input data.

## Features

- Detects the onset of new trends in financial data.
- Utilizes autocorrelation periodogram algorithm to determine the dominant cycle period.
- Applies high-pass filtering and super-smoothing to extract the underlying trend.
- Incorporates adaptive gain control (AGC) for noise reduction and signal amplification.
- Adjustable parameters for fine-tuning the indicator's performance.

## Usage

The EOT indicator can be applied to various financial instruments, such as stocks, currencies, commodities, and cryptocurrencies. It is particularly useful for identifying potential trend reversals or the beginning of new trends, enabling traders and investors to make informed decisions about entering or exiting positions.

To use the EOT indicator, you need to provide the following inputs:

- `input_data`: The time series data (e.g., stock prices) you want to analyze.
- `auto_avg`: The averaging period for autocorrelation calculations.
- `auto_min`: The minimum period for the dominant cycle detection.
- `auto_max`: The maximum period for the dominant cycle detection.
- `K`: The smoothing factor for the quotient calculation.

The indicator will output two arrays:

1. `Q`: The EOT indicator values.
2. `dominant_cycles`: The dominant cycle periods for each data point.

You can then plot the EOT indicator values alongside the original time series data to visualize the identified trends and make trading decisions based on the indicator's signals.

## Implementation

The EOT indicator is implemented using the Numba library for numerical computing in Python. Numba is a just-in-time (JIT) compiler that translates a subset of Python and NumPy code into fast machine code, providing significant performance improvements compared to pure Python implementations.

The implementation includes several helper functions:

- `nz`: Replaces zeros and NaN values with a small number to avoid division by zero errors.
- `high_pass_filter` and `high_pass_filter_2nd`: Apply high-pass filtering to the input data.
- `super_smoother`: Applies a super-smoother filter to the high-pass filtered data.
- `_auto_dom_imp`: Calculates the dominant cycle period using the autocorrelation periodogram algorithm.
- `agc`: Performs adaptive gain control on the filtered data.
- `quotient`: Calculates the final EOT indicator values using the AGC output and a smoothing factor.

The main `EOT` function orchestrates the execution of these helper functions and returns the EOT indicator values and dominant cycle periods.