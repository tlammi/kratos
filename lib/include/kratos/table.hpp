#pragma once

#include "kratos/row.hpp"

namespace kratos{

class Table{
public:
	template<typename HeaderIter>
	Table(HeaderIter iter, HeaderIter end){
		while(iter != end){
			column_names_.push_back(*iter);
			++iter;
		}
	}


	const std::vector<std::string_view>& header(){
		return column_names_;
	}

	Row& operator[](size_t idx){
		return rows_.at(idx);
	}
private:
	std::vector<std::string_view> column_names_{};
	std::vector<Row> rows_{};
};
}
