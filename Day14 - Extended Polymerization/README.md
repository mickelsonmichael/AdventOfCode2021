# Day 14 - Extended Polymerization

Today I utilized some really helpful methods/libraries in Python, including `setdefault` for adding to a map when the value doesn't already exist and a smidge of multi-threading.

My final solution doesn't have any multi-threading in it because I found a more optimal solution, but I wanted to give it a shot. Initially I was doing it in an inefficient way because I couldn't think of the best way to record the pairs (through some helpful tips online, I realized a dictionary of pairs is the solition), and I wanted to see if it was possible to complete using multi-threading in any sort of reasonable time. While it was running, I was doing some additional research and a helpful redditor pointed out that because of the exponential growth I would be processessing petabytes of data, which (obviously) isn't ideal. So I had to scrap my multi-threaded solution in favor of a dictionary. Regardless, it was still some good practice and a nice foray into the `threading` library.

Things I improved on today:

- Learned about the `threading` library
- Learned about the `setdefault` method
