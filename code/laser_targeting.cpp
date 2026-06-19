#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main(){
    int n;
    cin>>n;
    for (int i=0;i<n;i++){
        int h,w,t;
        cin >>h>>w>>t;
        //=======================================
        vector<vector<int>> coor(t,vector<int>(2,0));
        for(int j=0;j<t;j++){
            cin>>coor[j][0]>>coor[j][1];
        }

        //=======================================
        vector<vector<char>> tar(h+1,vector<char>(w+1,'.'));
        for(int j=1;j<=h;j++){
            for (int k=1;k<=w;k++){
                cin>>tar[j][k];
            }
        }
        //=======================================
        int count=0;
        for(int j=0;j<t;j++){
            int x=coor[j][0];
            int y=coor[j][1];
            if(tar[x][j]=='.') count++;
        }

        cout<<count<<endl;
    }
}