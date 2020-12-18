#include <iostream>

#include "kratos/app.hpp"

int main(){
	
	kratos::App a;
	std::cerr << a.event().name() << '\n';
}
