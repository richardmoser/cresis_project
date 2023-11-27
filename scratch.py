from functions import *
import matplotlib.pyplot as plt

# print out the twtt to depth conversion for 10ms, 20ms, 30ms, 40ms, 50ms, 60ms, 70ms, 80ms, 90ms, 100ms
# print to the nearest meter
print("twtt to depth conversion for refraction index 1.77:")
for i in range(1, 11):
    print(f"{i * 10} ms: {round(twtt_to_depth(i * 10 * 10 ** -6, 1.77))} m")
