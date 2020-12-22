#pragma once

#include <string_view>

namespace kratos{

enum class WeightUnit{
	Gram,
};

template<WeightUnit W, size_t Base> 
class Weight{
public:
	constexpr Weight(){}
	constexpr Weight(std::string_view str){
		
	}

private:
	Weight<W, 1> val_{};
};

template<WeightUnit W>
class Weight<W, 1>{
public:
	Weight(){}

	Weight& operator=(int i) noexcept {
		val_ = i;
		return *this;
	}

	operator int() noexcept {
		return val_;
	}
private:
	int val_{0};
};

}
