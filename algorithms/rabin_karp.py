def rabin_karp_search(text, pattern):
    positions = []
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return positions

    prime = 101
    base = 256
    pattern_hash = 0
    text_hash = 0
    power = 1

    for _ in range(m - 1):
        power = (power * base) % prime

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % prime
        text_hash = (text_hash * base + ord(text[i])) % prime

    for i in range(n - m + 1):
        if pattern_hash == text_hash and text[i:i + m] == pattern:
            positions.append(i)

        if i < n - m:
            text_hash = (
                base * (text_hash - ord(text[i]) * power)
                + ord(text[i + m])
            ) % prime

    return positions
