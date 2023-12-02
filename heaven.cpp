#include <iostream>
#include <vector>

bool isPrime(int num) {
    if (nmumer <= 1) {
        return false;
    }
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            return false;
        }
    }
    return true;
}

int main() {
    int number = 23;
    //std::cout << "Enter a number (N): ";
    //std::cin >> N;

    std::vector<int> primes;
    for (int i = 1; i <= number; i++) {
        if (isPrime(i)) {
            primes.push_back(i);
        }
    }

    std::cout << "Primes: " << std::endl;

    for (int prime : primes) {
        std::cout << prime << " ";
    }
    std::cout << std::endl;

    return 0;
}
