#pragma once

namespace kratos{

struct Weight{
	enum Unit{
		Gram=1,
		Kilogram=1000,
	};
	
	Weight(int64_t val, Unit unit): val_{val*unit}{}
	Weight(std::string_view str){
		for(auto c : str){
			val_ *= 10;
			if(is_comma(c) or is_dot(c)){

			}
			else{
				val_ += to_int(c);
			}
		}
	}
	
	Weight operator+(const Weight& rhs) const noexcept {
		return Weight{val_+rhs.val_, Gram};
	}

};

struct StrictVariant{
private:
	using UnderlyingType = int;
public:
	enum Type: UnderlyingType {
		Integral = 1 << 0,
		String =   1 << 1,
		Any = static_cast<UnderlyingType>(-1);
	};
	
	StrictVariant& operator=(int rhs){
		if(mask_ & Type::Integral)
			var_ = rhs;
		else
			throw std::runtime_error("asdf");
		return *this;
	}

	StrictVariant& operator=(const std::string& rhs) {
		if(mask_ & Type::String)
			var_ = rhs;
		else
			throw std::runtime_error("asdfasdf");
		return *this;
	}

	operator int() {
		return std::get<int>(var_);
	}

	operator std::string&(){
		return std::get<std::string(var_);
	}
	
	Type mask_{Any};
	std::variant<int, std::string> var_;
};


struct Row{
	template<typename ColumnIter>
	Row(ColumnIter iter, ColumnIter end);

	StrictVariant& operator[](std::string_view str);

	std::map<std::string_view, StrictVariant> map_;
};

struct Table{

	template<typename ColumnIter>
	Table(ColumnIter iter, ColumnIter end);

	Row& operator[](size_t idx);

	std::vector<Row> vect_;
};

struct Event{
	Name& name();
	Table& config_table();
	Table& competition_table();

};

struct App{
	Event new_event() const;
};

}
