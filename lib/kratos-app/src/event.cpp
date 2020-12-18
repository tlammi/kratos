#include "kratos/event.hpp"


namespace kratos{

Event::Event(){}

const std::string& Event::name() const{
	return name_;
}
}
