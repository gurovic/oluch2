#include <iostream>

using namespace std;

int main()
{
    int n,s=0,i;
    float p;
    cin>>n;
    for(i=1;i<=n;i++)
    {
        cin>>p;
        s+=p;
    }
    cout<<s<<endl;

    return 0;
}
