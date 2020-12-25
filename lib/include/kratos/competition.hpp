#pragma once

#include <vector>
#include <string_view>

namespace kratos{

class Competition{
public:
	Competition();
	virtual ~Competition();
	virtual std::string_view name() const = 0;

private:
};
}
