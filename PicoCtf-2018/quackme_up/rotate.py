INT_BITS = 8
ROR = 4
def rightRotate(n, d):
    return (n >> d) | (n << (INT_BITS - d))

def keep8bits(number):
    return (((1 << 8) - 1) & number)


encrypted = "118020E0225372A101415520A0C025E33540659575003085C1"
i = 0
for i in range(0, len(encrypted), 2):
    n = (int(encrypted[i] + encrypted[i+1], 16) ^ 22)
    print(chr(keep8bits(rightRotate(n, ROR))), end = '')
