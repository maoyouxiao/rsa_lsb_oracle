#!/usr/bin/python3
# -*- coding: utf-8 -*-

def wait():
    import sys
    ch = ["|", "/", "-", "\\"]
    def f():
        i = 0
        while True:
            yield ch[i]
            i += 1
            if i == len(ch):
                i = 0
    w = f()
    def p():
        sys.stdout.write(next(w)+"\b")
    return p

def fuck(oracle, c, e, n):
    w = wait()
    l = 0
    r = n
    while l != r:
        c = (pow(2, e, n) * c) % n
        if oracle(c) & 1:
            l = (l + r) // 2
        else:
            r = (l + r) // 2
        w()
    return l, r

def fix(l, c, e, n):
    for i in range(-128, 128):
        if pow(l+i, e, n) == c:
            return l+i
    return None

if __name__ == "__main__":
    import re
    import binascii
    from pwn import *

    p = process(["python2", "./backdoor_ctf_2018_bit_leaker/service.py"])

    def oracle(c):
        flag = 0
        for i in range(10):
            p.sendline(str(c))
            s = p.recv()
            if int(re.findall(b"l\s*=\s*([0-9]*)", s)[0]) & 1:
                flag = 1
        return flag

    ss = p.recv()
    N = int(re.findall(b"N\s*=\s*(\d+)", ss)[0])
    e = int(re.findall(b"e\s*=\s*(\d+)", ss)[0])
    c = int(re.findall(b"c\s*=\s*(\d+)", ss)[0])
    print("N =", N)
    print("e =", e)
    print("c =", c)

    l, r = fuck(oracle, c, e, N)

    print("l = " + hex(l))
    print("r = " + hex(r))

    l = fix(l, c, e, N)
    if not l:
        l = r
    print("result:", binascii.unhexlify(hex(l)[2:]))
