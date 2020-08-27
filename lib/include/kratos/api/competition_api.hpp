#pragma once

namespace kratos{
namespace api{
class CompetitionApi{
public:
	static CompetitionApi new_competition();
	static CompetitionApi load_competition(const std::filesystem::path& path);
	void save(const std::filesystem::path& path);

private:
	CompetitionApi();
};
}
}
