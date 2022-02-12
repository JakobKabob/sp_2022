#include <iostream>
#include <cmath>
#include <string>


void forloop_pyramid(int height) {
    std::cout << "Implementation: regular forloop" << std::endl; 
    int width = height*2-1;
    for (int i = 1; i <= width; i++){
        int column_height = height - abs(height - i); 

        for (int _ = 0; _ < column_height; _++){
            std::cout << "*";
        }
        std::cout << std::endl;
    } 
}

void forloop_pyramid_inverse(int height) {
    std::cout << "Implementation: inverse forloop" << std::endl; 
    int width = height*2-1;
    for (int i = 1; i <= width; i++){
        int column_height = height - abs(height - i); 

        // std::string(int, " ") werkte niet :( clang fout
        std::string spaces;
        for (int _ = 0; _ < height - column_height; _++){
            spaces.append(" ");
        }
        std::cout << spaces;

        for (int _ = 0; _ < column_height; _++){
            std::cout << "*";
        }
        std::cout << std::endl;
    } 
}

void whileloop_pyramid(int height) {
    std::cout << "Implementation: regular whileloop" << std::endl; 

    bool reached_peek = false;
    int i = 1;
    while (i > 0) {
        int c = 0;
        while (c < i) {
            std::cout << "*";
            c++;
        }

        if (i == height) {
            reached_peek = true;
        }
        if (reached_peek) {
            i--;
        } else {
            i++;
        }
        std::cout << std::endl;
    }
}

void whileloop_pyramid_inverse(int height) {
    std::cout << "Implementation: inverse whileloop" << std::endl; 

    bool reached_peek = false;
    int i = 1;
    while (i > 0) {

        // std::string(int, " ") werkte niet :( clang fout
        std::string spaces;
        for (int _ = 0; _ < height - i; _++){
            spaces.append(" ");
        }
        std::cout << spaces;

        int c = 0;
        while (c < i) {
            std::cout << "*";
            c++;
        }

        if (i == height) {
            reached_peek = true;
        }
        if (reached_peek) {
            i--;
        } else {
            i++;
        }
        std::cout << std::endl;
    }
}


int get_height() {
    int height;
    std::cout << "Hoe groot? ";
    std::cin >> height;

    return height;
}

// cli args uitproberen
int main(int argc, char *argv[]) {
    switch (argc) {
        case 2: 
            if (argv[1] == std::string("while")) {
                whileloop_pyramid(get_height());
            } else if (argv[1] == std::string("for")) {
                forloop_pyramid(get_height());
            } else {
                std::cout << "unknown argument \"" << argv[1] << "\"" << std::endl;
            }
            break;
        case 3: 
            if (argv[2] == std::string("inverse")) {
                if (argv[1] == std::string("while")) {
                    whileloop_pyramid_inverse(get_height());
                } else if (argv[1] == std::string("for")) {
                    forloop_pyramid_inverse(get_height());
                } else {
                    std::cout << "unknown argument \"" << argv[1] << "\"" << std::endl;
                }
            } else {
                std::cout << "Unknown argument \"" << argv[2] << "\"" << std::endl;
            }
            break;
        default:
            std::cout << "commandline arguments: for/while (inverse)" << std::endl;
            forloop_pyramid(get_height());

        return 0;
    }
}
