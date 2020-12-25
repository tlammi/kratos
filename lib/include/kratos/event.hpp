#pragma once

#include <string>
#include <string_view>
#include <iostream>


#include "kratos/competition.hpp"

namespace kratos{

class Event{
public:
	Event();
	constexpr std::string_view name() const {
		return "Dummy Event";
	}

private:
};
}

