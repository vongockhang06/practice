#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main(){
    int n;
    string exit;
    cin>>n;
    cin>>exit;
    int k=exit.size();
    int step=1;
    int layer=-1;
    for(int i=0;i<k;i++){
        layer+=2;
        if(i==0) continue;
        int len=layer*2-1;
        char prev=exit[i-1];
        char now=exit[i];
        if(prev=='L' && now=='R' || prev=='R' && now=='L' 
            || prev=='D' && now=='U' || prev=='U' && now=='D'){
                step=step+ len + (len/2)*2 +1;
        }
        else if(prev=='L' && now=='L' || prev=='R' && now=='R' 
            || prev=='D' && now=='D' || prev=='U' && now=='U'){
                step+=2;
            }
        else if(prev=='L' && now=='D' || prev=='L' && now=='U' 
            || prev=='R' && now=='D' || prev=='R' && now=='U' ||
            prev=='D' && now=='L' || prev=='D' && now=='R' 
            || prev=='U' && now=='L' || prev=='U' && now=='R'){
                step=step+len+1;
            }

    }
    cout<<step<<endl;
}