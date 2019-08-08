#include <iostream>
#include <cstdlib>
#include <assert.h>

using namespace std;

int *dp = nullptr;
char *magic = nullptr;

int sol(int step, int off) {
    if (step == 99) 
        return magic[(off + (step * (step + 1)/2 ))];

    if (!dp[100 * step + off]) 
        dp[100 * step + off] = magic[(off + (step * (step + 1)/2 ))] \
        + max( \
            sol(step + 1, off), \
            sol(step + 1, off + 1));
    return dp[100 * step + off] ;
}

int printflag() {
    int off = 0, res = 0;
    for (int i = 0; i < 100; i++) {
        res += magic[(off + (i * (i + 1)/2 ))];
        cout << magic[(off + (i * (i + 1)/2 ))];
        if (i == 99) break;
        if (dp[100 *(i + 1) + off + 1] > dp[100 * (i + 1) + off])
            off++;
    }
    cout << endl;
    return res;
}

int main()
{
    dp = (int *)calloc(4, 100 * 100);
    magic = (char *)malloc(5050);
    
    FILE *fp = fopen("./magic", "rb");
    assert (fp >= 0);
    fread(magic, 1, 5050, fp);

    cout << sol(0, 0) << endl;
    cout << printflag() << endl;
    return 0;
}