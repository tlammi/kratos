#pragma once

#include <string>
#include <array>
#include "kratos/data/weight.hpp"
#include "kratos/data/date.hpp"
#include "kratos/data/lift.hpp"

namespace kratos{
namespace data{

struct Lifts{
	std::array<Lift, 3> snatches{};
	std::array<Lift, 3> cjs{};
};

struct Competitor{
	std::string first_name{};
	std::string last_name{};
	Weight body_weight{};
	Date date_of_birth{};
	Lifts lifts{};
};

}
}
