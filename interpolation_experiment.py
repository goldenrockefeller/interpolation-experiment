import numpy as np

def kaiser(L, f, a):
    # from https://en.wikipedia.org/wiki/Kaiser_window
    side = (
        np.sqrt(
            (np.pi * a) ** 2
            -(np.pi * L * f) ** 2
        )
    )
    return (
        np.sinh(side)
        / (
            np.i0(np.pi * a)
            * side
        )
    )

def kaiser2(L, f, a):
    # from https://en.wikipedia.org/wiki/Kaiser_window
    side = (
        np.sqrt(
            (np.pi * L * f) ** 2
            - (np.pi * a) ** 2
        )
    )
    return (
        np.sin(side)
        / (
            np.i0(np.pi * a)
            * side
        )
    )

sample_rate = 48000 * 8
cutoff_hz = 24000
window_len = 6

nyquist = 0.5

cutoff = cutoff_hz / sample_rate

transition_width = 1 - 2* cutoff
first_noise = 1- cutoff

# "a" from https://en.wikipedia.org/wiki/Rectangular_function
# is sinc_pass_factor
sinc_pass_freq = 0.5

# "alpha" from https://en.wikipedia.org/wiki/Kaiser_window
# is kaiser_factor
kaiser_null = first_noise
kaiser_factor = np.sqrt((window_len * kaiser_null) ** 2 - 1 )

print(f"{kaiser_null=}")
print(f"{kaiser_factor=}")

conv_multiplier = 2 * sinc_pass_freq
test_freqs = np.arange(1000) / 1000 + 0.5
#test_amps =  kaiser(window_len, test_freqs, kaiser_factor)
#print(np.max(20 * np.log10(np.abs(test_amps))))

middle = 0.5 / window_len * (np.sqrt(2 + kaiser_factor ** 2) + np.sqrt(1 + kaiser_factor ** 2))
k0 = np.abs(kaiser(window_len, 0 , kaiser_factor))
print(
    20 * np.log10(np.abs(kaiser(window_len, middle , kaiser_factor)  / k0)),
    20 * np.log10(np.abs(kaiser2(window_len, middle , kaiser_factor) / k0))
)
print("Deviation")
print(
    20 * np.log10(np.abs(kaiser(window_len, cutoff , kaiser_factor) / k0)),
    20 * np.log10(np.abs(kaiser2(window_len, cutoff , kaiser_factor) / k0))
)
print("--------------------------------")

# "alpha" from https://en.wikipedia.org/wiki/Kaiser_window
# is kaiser_factor
kaiser_null = transition_width / 2
kaiser_factor = np.sqrt((window_len * kaiser_null) ** 2 - 1 )

print(f"{kaiser_null=}")
print(f"{kaiser_factor=}")

conv_multiplier = 2 * sinc_pass_freq
test_freqs = np.arange(1000) / 1000 + 0.5
#test_amps =  kaiser(window_len, test_freqs, kaiser_factor)
#print(np.max(20 * np.log10(np.abs(test_amps))))

middle = 0.5 / window_len * (np.sqrt(2 + kaiser_factor ** 2) + np.sqrt(1 + kaiser_factor ** 2))
k0 = np.abs(kaiser(window_len, 0 , kaiser_factor))
print(20 * np.log10(np.abs(kaiser(window_len, middle , kaiser_factor)  / k0)))
print(20 * np.log10(np.abs(kaiser2(window_len, middle , kaiser_factor) / k0)))

n = 2
sin = np.sin
tri =20 * np.log10(
 ((sin(np.pi * cutoff) / np.pi/cutoff) / (sin(np.pi * first_noise) / np.pi/first_noise))**n
)
n= 4
quad =20 * np.log10(
 ((sin(np.pi * cutoff) / np.pi/cutoff) / (sin(np.pi * first_noise) / np.pi/first_noise))**n
)
print(f"{tri=}")
print(f"{quad=}")

def kaiser_spectum(L, beta, f):

    uf = complex(1, 0) * 2 * np.pi * f
    return (
        abs(
            (L * np.sinh(beta * np.sqrt(1 - (L * 0.5 * uf/beta) ** 2)))
            / (np.i0(beta) * beta * np.sqrt(1 - (L * 0.5 * uf/beta) ** 2))
        )
    )
