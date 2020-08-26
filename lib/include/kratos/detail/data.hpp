#pragma once

#include <string>

namespace kratos{

struct CompetitionData{
	std::string competition_name{};

};

CompetitionData create_competition();
CompetitionData load_competition(const std::filesystem::path& file);

void save_competition(const std::filesystem::path& file, const CompetitionData& data);
bool in_sync(const std::filesystem::path& file, const CompetitionData& data);

}
