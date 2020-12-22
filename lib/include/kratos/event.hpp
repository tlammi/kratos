#pragma once

#include <string>
#include <string_view>
#include <iostream>

#include "kratos/nameview.hpp"

namespace kratos{

class Event{
public:
	Event();

	NameView& name_view();

private:
	NameView name_view_{};
};
}

