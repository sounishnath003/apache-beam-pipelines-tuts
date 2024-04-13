import java.util.Arrays;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
}

class Solution {
    public int numDistinct(String s, String t) {
        int n = s.length();
        int m = t.length();
        int[][] dp = new int[n + 1][m + 1];
        for (int i = 0; i <= m; i++) {
            dp[i][0] = 1;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                char a = s.charAt(i - 1);
                char b = t.charAt(j - 1);
                if (a == b) {
                    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
                } else {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }
        print(dp);
        return dp[n][m];
    }

    private int f(String s, String t, int i, int j, int[][] dp) {
        if (j == 0) {
            return 1;
        }
        if (i == 0) {
            return 0;
        }
        char a = s.charAt(i);
        char b = t.charAt(j);

        if (a == b) {
            return dp[i][j] = f(s, t, i - 1, j - 1, dp) + f(s, t, i - 1, j, dp);
        }

        return dp[i][j] = f(s, t, i - 1, j, dp);
    }

    private void print(int[][] dp) {
        for (int[] row : dp) {
            System.out.println(Arrays.toString(row));
        }
    }
}