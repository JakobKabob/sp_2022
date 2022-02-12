#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

void first_deviation(string str1, string str2) {
    for (int i = 0; i < max(str1.length(), str2.length());i++ ) { 
        if (str1[i] != str2[i]) {
            cout << "Het eerste verschil zit op index: " << i << endl;
            return;
        }
    }

    cout << "Geen verschil joh" << endl;
    return;
}

int main() {
    string str1; cout << "Geef een string: "; cin >> str1;
    string str2; cout << "Geef een string: "; cin >> str2;

    first_deviation(str1,str2);

    return 0;
}
