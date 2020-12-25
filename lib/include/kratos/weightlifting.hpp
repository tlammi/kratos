#pragma once

#include <string_view>

#include "kratos/competition.hpp"

namespace kratos{

class Weightlifting: public Competition {
public:
	Weightlifting();

	std::string_view name() const final;

private:
	static inline std::string_view name_{"Weightlifting"};
};

}
