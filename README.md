# Autocorrelation Early Onset Trend (AEOT) Indicator

![Showcase Image]([https://github.com/valazeinali/Valatility-Crypto-Gang/blob/main/assets/Valatility.png](https://github.com/NoturBusiness/Autocorrelation-EarlyOnsetTrend/blob/main/showcase.png))

[APA-Adaptive, Ehlers Early Onset Trend [Loxx] — Indicator by loxx — TradingView](https://www.tradingview.com/script/ieVGZXw5-APA-Adaptive-Ehlers-Early-Onset-Trend-Loxx/)
## Features

- Detects the onset of new trends in financial data.
- Utilizes autocorrelation periodogram algorithm to determine the dominant cycle period.
- Applies high-pass filtering and super-smoothing to extract the underlying trend.
- Incorporates adaptive gain control (AGC) for noise reduction and signal amplification.
- Adjustable parameters for fine-tuning the indicator's performance.

## Usage

The AEOT indicator can be applied to various financial instruments, such as stocks, currencies, commodities, and cryptocurrencies. It is particularly useful for identifying potential trend reversals or the beginning of new trends, enabling traders and investors to make informed decisions about entering or exiting positions.

To use the AEOT indicator, you need to provide the following inputs:

- `input_data`: The time series data (e.g., stock prices) you want to analyze.
- `auto_avg`: The averaging period for autocorrelation calculations.
- `auto_min`: The minimum period for the dominant cycle detection.
- `auto_max`: The maximum period for the dominant cycle detection.
- `K`: The smoothing factor for the quotient calculation.

The indicator will output two arrays:

1. `Q`: The AEOT indicator values.
2. `dominant_cycles`: The dominant cycle periods for each data point.

You can then plot the AEOT indicator values alongside the original time series data to visualize the identified trends and make trading decisions based on the indicator's signals.

## Implementation

The AEOT indicator is implemented using the Numba library for numerical computing in Python. Numba is a just-in-time (JIT) compiler that translates a subset of Python and NumPy code into fast machine code, providing significant performance improvements compared to pure Python implementations.

The implementation includes several helper functions:

- `nz`: Replaces zeros and NaN values with a small number to avoid division by zero errors.
- `high_pass_filter` and `high_pass_filter_2nd`: Apply high-pass filtering to the input data.
- `super_smoother`: Applies a super-smoother filter to the high-pass filtered data.
- `_auto_dom_imp`: Calculates the dominant cycle period using the autocorrelation periodogram algorithm.
- `agc`: Performs adaptive gain control on the filtered data.
- `quotient`: Calculates the final AEOT indicator values using the AGC output and a smoothing factor.

The main `AEOT` function orchestrates the execution of these helper functions and returns the AEOT indicator values and dominant cycle periods.
