#include "kratos/app.hpp"

namespace kratos{

App::App(){}

Event App::new_event() const {
	return Event();
}
}
