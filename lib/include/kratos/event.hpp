#pragma once

#include <string>
#include <string_view>
#include <vector>


#include "kratos/table.hpp"

namespace kratos{

class Event{
public:
	Event();
	constexpr std::string_view name() const {
		return "Dummy Event";
	}

	
	Table& config_table(){
		return config_table_;
	}
	

private:
	static const inline std::vector<std::string_view> COLUMN_NAMES{
		"Last Name",
		"First Name",
		"Body Weight",
		"Date of Birth",
		"Snatch Start",
		"C&J Start",
	};
	Table config_table_{COLUMN_NAMES.begin(), COLUMN_NAMES.end()};
};
}

