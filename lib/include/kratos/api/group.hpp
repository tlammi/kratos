#pragma once

namespace kratos{
namespace api{
class Competition;

class Group{
friend class Competition;
public:
	int create();
	void remove(int id);

private:
	Group();
};
}
}
