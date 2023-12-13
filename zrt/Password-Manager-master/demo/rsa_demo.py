def gcd(a, h):
    temp = 0
    while True:
        temp = a % h
        if temp == 0:
            return h
        a = h
        h = temp


def extended_gcd(a, b):  # a*x + b*y = 1
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y


def main():
    p = 37
    q = 13
    n = p * q
    eula = (p-1) * (q-1)

    e = 2

    while e < eula:
        if gcd(e, eula) == 1:
            break
        else:
            e += 1

    # Private key
    _, b, a = extended_gcd(e, -eula)

    if b < 0 and a < 0:
        b += eula
        a += e

    print(f"e = {e}, eula = {eula}")
    print(f"a = {a}, b = {b}")
    print(f"{b} * {e} = {a} * {eula} + 1")
    print(f"n = p * q: {n} = {p} * {q}")

    while True:
        print("---------------------------------")
        to_encrypt = int(input("> Number to encrypt: "))
        print(f"Original Message: {to_encrypt}")

        encrypted = pow(to_encrypt, e, n)
        print(f"Encrypted Message: {encrypted}")

        decrypted = pow(encrypted, b, n)
        print(f"Decrypted Message: {decrypted}")
        print(f"Decrypted Message: {decrypted} + {n} * Z")


main()
