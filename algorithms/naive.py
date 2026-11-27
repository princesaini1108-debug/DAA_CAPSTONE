def naive_search(text, pattern):
    positions = []
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return positions

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            positions.append(i)

    return positions
