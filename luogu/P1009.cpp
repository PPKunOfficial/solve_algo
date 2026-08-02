
#include <cstddef>
#include <iomanip>
#include <iostream>
#include <vector>
struct BigInt {
    static constexpr int BASE = 1e9;
    std::vector<int> a;

    BigInt(long long v = 0) {
        if (v == 0)
            a.push_back(0);
        while (v > 0) {
            a.push_back(v % BASE);
            v /= BASE;
        }
    }

    void trimz() {
        while (a.size() > 1 && a.back() == 0)
            a.pop_back();
    }

    BigInt& operator*=(long long b) {
        long long carry = 0;
        for (size_t i = 0; i < a.size() || carry; i++) {
            if (i == a.size())
                a.push_back(0);
            long long cur = (long long)a[i] * b + carry;
            a[i] = cur % BASE;
            carry = cur / BASE;
        }
        trimz();
        return *this;
    }

    BigInt operator*(long long b) const {
        BigInt res = *this;
        res *= b;
        return res;
    }

    BigInt& operator+=(const BigInt& b) {
        long long carry = 0;
        size_t n = std::max(a.size(), b.a.size());
        for (size_t i = 0; i < n || carry; ++i) {
            if (i == a.size())
                a.push_back(0);
            if (i < b.a.size())
                carry += b.a[i];
            carry += a[i];
            a[i] = carry % BASE;
            carry /= BASE;
        }
        return *this;
    }

    BigInt operator+(const BigInt& b) const {
        BigInt res = *this;
        res += b;
        return res;
    }

    friend std::ostream& operator<<(std::ostream& os, const BigInt& num) {
        if (num.a.empty())
            return os << 0;
        os << num.a.back();
        for (int i = (int)num.a.size() - 2; i >= 0; --i) {
            os << std::setw(9) << std::setfill('0') << num.a[i];
        }
        return os;
    }
};

int main() {
    int n;
    std::cin >> n;
    BigInt res = 0;
    for (int i = 1; i <= n; i++) {
        BigInt p = 1;
        for (int j = 1; j <= i; j++) {
            p *= j;
        }
        res += p;
    }
    std::cout << res;
    return 0;
}