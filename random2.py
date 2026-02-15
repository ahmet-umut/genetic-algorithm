import ctypes
from ctypes import wintypes
import random

ntdll = ctypes.WinDLL('ntdll')

# NtAllocateVirtualMemoryEx signature
NtAllocateVirtualMemoryEx = ntdll.NtAllocateVirtualMemoryEx
NtAllocateVirtualMemoryEx.restype = wintypes.LONG  # NTSTATUS
NtAllocateVirtualMemoryEx.argtypes = [
    wintypes.HANDLE,      # ProcessHandle
    ctypes.POINTER(ctypes.c_void_p),  # BaseAddress
    ctypes.POINTER(ctypes.c_size_t),  # RegionSize
    wintypes.ULONG,       # AllocationType
    wintypes.ULONG,       # PageProtection
    ctypes.c_void_p,      # ExtendedParameters (NULL for basic use)
    wintypes.ULONG        # ExtendedParameterCount
]

# Constants
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04
CURRENT_PROCESS = ctypes.c_void_p(-1)

base_address = ctypes.c_void_p(0)  # NULL lets ASLR choose
region_size = ctypes.c_size_t(4096)  # One page
    
status = NtAllocateVirtualMemoryEx(
    CURRENT_PROCESS,
    ctypes.byref(base_address),
    ctypes.byref(region_size),
    MEM_COMMIT | MEM_RESERVE,
    PAGE_READWRITE,
    None,
    0
)
    
if status != 0:
    raise OSError(f"NtAllocateVirtualMemoryEx failed: {status:#x}")
    
# Extract randomness from ASLR-assigned address
address = base_address.value
    
# Free the memory
NtFreeVirtualMemory = ntdll.NtFreeVirtualMemory
MEM_RELEASE = 0x8000
size = ctypes.c_size_t(0)
NtFreeVirtualMemory(CURRENT_PROCESS, ctypes.byref(base_address), ctypes.byref(size), MEM_RELEASE)

print(f"Random address: {address:#x}")

random_bits = (address >> 32) & 0xFF
random_bit_size = 8
max_random_bit_size = 8

from siphash24 import siphash24

def spread_even(x, power):
	for i in range(power-1, -1, -1):
		x = (x | (x << 2**i)) & int(f"0b{("0"*(2**i) + "1"*(2**i)) * 2**(power-i-1)}", 2)
	return x

def spread_odd(x, power):
	return spread_even(x, power) << 1

def morton_encode_2d(x, y, power):
	return spread_even(x, power) | spread_odd(y, power)

def scatter_to_mask(x, mask):
    result = 0
    bit_idx = 0
    for i in range(mask.bit_length()):
        if (mask >> i) & 1:
            if (x >> bit_idx) & 1:
                result |= 1 << i
            bit_idx += 1
    return result

def produce():
    global random_bits, random_bit_size, max_random_bit_size
    """
    x = random_bits >> 4 & 0xf
    y = random_bits & 0xf
    random_bits += morton_encode_2d(x, y, 4)
    """
    random_bits ^= scatter_to_mask(random_bits, 0b10100001)
    random_bits ^= scatter_to_mask(random_bits, 0b1)
    random_bits ^= scatter_to_mask(random_bits, 0b01011110)
    random_bits ^= (random_bits & 0b100000 > 0) * 0b1101001
    #random_bit_size = (max_random_bit_size := max_random_bit_size+1)
    random_bit_size = max_random_bit_size
    return random_bits

def bit():
    global random_bits, random_bit_size
    #print(f"Random bits: {random_bits:#x}, size: {random_bit_size}")
    if not random_bit_size:
        produce()
        #print(f"Producing more random bits: {produce():#x}")
    random_bit_size -= 1
    bit = random_bits & 1<<random_bit_size > 0
    return bit

def rrange(stop):
    global random_bits
    if stop <= 0:
        raise ValueError("stop must be positive")
    bits_needed = (stop - 1).bit_length()
    while True:
        result = 0
        for d in range(bits_needed-1, -1, -1):
            result += bit() << d
            if result >= stop:
                break
        else:
            return result