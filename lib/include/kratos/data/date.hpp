#pragma once

#include <string_view>

namespace kratos{
namespace data{

class Date{
public:
	Date();
	Date(std::string_view str);

	static Date now();
	
	bool operator==(const Date& rhs) const {
		return year == rhs.year && 
		       month == rhs.month &&
		       day == rhs.day;
	}

	bool operator<(const Date& rhs) const {
		if(year == rhs.year){
			if(month == rhs.month)
				return day < rhs.day;
			return month < rhs.month;
		}
		return year < rhs.year;
	}

	bool operator>(conts Date& rhs) const {
		if(year == rhs.year){
			if(month == rhs.month)
				return day > rhs.day;
			return month > rhs.month;
		}
		return year > rhs.year;
	}

	bool operator<=(const Date& rhs) const{
		return *this < rhs || *this == rhs;
	}

	bool operator>=(const Date& rhs) const {
		return *this > rhs || *this == rhs;
	}

	bool operator!=(const Date& rhs) const {
		return !(*this == rhs);
	}

	std::string str() const{
		std::stringstream str{};
		str << day << '.' << month << '.' << year;
		return str.str();
	}
private:
	int year{0};
	int month{0};
	int day{0};
};

}
}
