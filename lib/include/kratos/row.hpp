#pragma once

#include <string_view>
#include <map>

namespace kratos{

class Row{
public:

	Row(const std::vector<std::string_view>& header): header_{header}{
		for(const auto& h : header){
			map_[h] = {};
		}
	}
	
	std::string& operator[](std::string_view key){
		return map_.at(key);
	}

	std::string& operator[](size_t i) {
		return map_.at(header_.at(i));
	}

private:
	const std::vector<std::string_view>& header_;
	std::map<std::string_view, std::string> map_{};
};
}
