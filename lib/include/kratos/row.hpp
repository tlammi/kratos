#pragma once

#include <string_view>
#include <map>

namespace kratos{

class Row{
public:
	template<typename ColumnIter>
	Row(ColumnIter iter, ColumnIter end){
		while(iter != end){
			map_[*iter] = {};
			++iter;
		}
	}
	
	std::string& operator[](std::string_view key){
		return map_.at(key);
	}
private:
	std::map<std::string_view, std::string> map_{};
};
}
