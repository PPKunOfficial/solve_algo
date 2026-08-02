
#include <cstring>
#include <iostream>
#include <vector>

struct Carpet {
    int a, b, g, k;
};

int main() {
    int n;
    Carpet ip;
    std::vector<Carpet> carpet(0);

    std::cin >> n;

    // 输入地毯
    for (int i = 0; i < n; i++) {
        std::cin >> ip.a >> ip.b >> ip.g >> ip.k;
        carpet.push_back(ip);
    }

    int x, y;
    std::cin >> x >> y;

    for (int i = carpet.size(); i > 0; i--) {
        int idx = i - 1;
        int a = carpet[idx].a;
        int b = carpet[idx].b;
        int g = carpet[idx].g;
        int k = carpet[idx].k;
        if (x >= a && x <= a + g && y >= b && y <= b + k) {
            std::cout << i;
            return 0;
        }
    }
    std::cout << -1;
    return 0;
}