#pragma once

namespace kratos{
namespace api{
class CompetitionApi;

class GroupApi{
friend class CompetitionApi;
public:
	int create();
	void remove(int id);

private:
	GroupApi();
};
}
}
