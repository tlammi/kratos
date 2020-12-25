#include "kratos/weightlifting.hpp"

#include <iostream>

namespace kratos{

Weightlifting::Weightlifting(): Competition{}{
	std::cerr << "constructing " << name_ << '\n';
}


std::string_view Weightlifting::name() const {
	return name_;
}

}
