#include <cstdio>
#include <iostream>

using namespace std;

int main() {
    int s, v;
    cin >> s >> v;

    int walk_time = (s + v - 1) / v;
    int total_time = walk_time + 10;

    int rest_minutes = (1920 - total_time) % 1440;

    int hh = rest_minutes / 60;
    int mm = rest_minutes % 60;

    printf("%02d:%02d\n", hh, mm);

    return 0;
}