#pragma once

namespace kratos{

class Discipline{
public:
	virtual std::string_view name() const = 0;
private:

};
}
