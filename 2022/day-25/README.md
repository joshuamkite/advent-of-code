we can populate a dictionary with lookup values for the basic equivalent and conversions of the mathematical signs and we will need to actually also implement a base 5 counting system. I did consider using [int for base conversion](https://mathspp.com/blog/base-conversion-in-python) but I found it more fiddly than coding directly given the minus digits. 


1. **Base-5 System**: The SNAFU system operates similarly to base-5, except the digits are `2, 1, 0, -, =`, where:
   - `2` represents 2
   - `1` represents 1
   - `0` represents 0
   - `-` represents -1
   - `=` represents -2

   Each position corresponds to powers of 5 (ones, fives, twenty-fives, etc.).

2. **Conversion to Decimal**: To convert a SNAFU number to decimal, you'd need to:
   - Start from the rightmost digit, which represents the ones place (5^0), and move leftward.
   - Multiply each SNAFU digit by the corresponding power of 5.
   - Sum the values.

3. **Reverse Conversion**: To convert a decimal number back to SNAFU:
   - Determine how the decimal number can be expressed using powers of 5.
   - Instead of using digits like 4 or 3 (which SNAFU doesn't support), you adjust the next higher place, using `2`, `1`, `0`, `-`, or `=` as needed.

4. **Handling Negative Digits**: The key difference with SNAFU is that it allows negative values for some digits. This means you might need to "borrow" from higher places, similar to how subtraction works with borrowing in normal base systems.

