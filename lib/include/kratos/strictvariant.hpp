#pragma once

namespace kratos{

class StrictVariant{
public:
	enum Type{
		Integer = 1 << 0,
		String  = 1 << 1,
	};
private:
};
}

