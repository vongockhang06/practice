#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
using namespace std;
int main(){
    int n;//test case;
    cin>>n;
    for(int i=0;i<n;i++){
        int H,W,Ph,Pw,mode;
        cin>> H>>W>>Ph>>Pw>>mode;
        vector<vector<int>> image(H,vector<int>(W,0));
        for(int j=0;j<H;j++){
            for(int k=0;k<W;k++){
                cin>>image[j][k];
            }
        }

        vector<vector<int>> res;
        for(int j=0;j<H;j+=Ph){
            vector<int> temp_res;
            for(int k=0;k<W;k+=Pw){
                vector<int> temp;
                for(int subj=j;subj<j+Ph;subj++){
                    for(int subk=k;subk<k+Pw;subk++){
                        temp.push_back(image[subj][subk]);
                    }
                }
                int element;
                if(mode==1){
                    auto max_it=max_element(temp.begin(),temp.end());
                    element=*max_it;
                }
                else if(mode==2){
                    auto min_it=min_element(temp.begin(),temp.end());
                    element=*min_it;
                }
                else{
                    int sum=accumulate(temp.begin(),temp.end(),0);
                    element=sum/temp.size();
                }
                temp_res.push_back(element);
            }
            res.push_back(temp_res);
        }

        int a=H/Ph;
        int b=W/Pw;
        for(int j=0;j<a;j++){
            for(int k=0;k<b;k++){
                cout<<res[j][k];
                if(k!=(b-1)) cout<<' ';
            }
            cout<<endl;
        }

    }
}