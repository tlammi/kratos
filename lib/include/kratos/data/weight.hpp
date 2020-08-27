#pragma once

namespace kratos{
namespace data{
class Weight{
public:
	Weight();
	Weight(int val, int exp);
	static Weight kg(int val){return Weight{val, 3};}
	
	std::string str(int exp);

private:
	int grams_{};
};
}
}
