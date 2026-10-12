# Assignment 2
# Question 8 - Matrix Path Optimizer with Dynamic Programming

MOD = 1000000007

def main():
    n, m = map(int, input().split())
    matrix = []

    for i in range(n):
        row = input().split()
        matrix.append(row)

    if matrix[0][0] == "X" or matrix[n - 1][m - 1] == "X":
        print("IMPOSSIBLE")
        return

    dp = [[None] * m for _ in range(n)]
    ways = [[0] * m for _ in range(n)]

    dp[0][0] = int(matrix[0][0])
    ways[0][0] = 1

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == "X":
                continue

            if i == 0 and j == 0:
                continue

            value = int(matrix[i][j])
            best = None
            count = 0

            for pi, pj in [(i, j - 1), (i - 1, j), (i - 1, j - 1)]:
                if pi >= 0 and pj >= 0 and dp[pi][pj] is not None:
                    if best is None or dp[pi][pj] > best:
                        best = dp[pi][pj]
                        count = ways[pi][pj]
                    elif dp[pi][pj] == best:
                        count = (count + ways[pi][pj]) % MOD

            if best is not None:
                dp[i][j] = best + value
                ways[i][j] = count

    if dp[n - 1][m - 1] is None:
        print("IMPOSSIBLE")
    else:
        print(dp[n - 1][m - 1], ways[n - 1][m - 1])


if __name__ == "__main__":
    main()