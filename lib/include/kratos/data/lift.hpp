#pragma once

#include "kratos/data/weight.hpp"

namespace kratos{
namespace data{
struct Lift{
	enum class Status{
		NotTried,
		Success,
		Fail
	};

	Weight weight;
	Status status;
};
}
}
