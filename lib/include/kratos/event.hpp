#pragma once

#include <string>

namespace kratos{

class Event{
public:
	Event();
	const std::string& name() const;
private:
	std::string name_{"Dummy Event"};
};
}
