
def recursion(n):
    dp = [None] * n
    dp[0] = 9029
    dp[1] = 9030
    dp[2] = 9033
    dp[3] = 9038
    dp[4] = 9045
    for i in range(5, n):
        dp[i] = (((dp[i - 1] - dp[i - 2]) + (dp[i - 3] - dp[i - 4])) + dp[i - 5]*4660) & 0xffffffff
        #print(dp[i])

    print(dp[n-1])

recursion(104806)

