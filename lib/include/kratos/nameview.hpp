#pragma once

#include <functional>
#include <string_view>
#include <string>

namespace kratos{

class NameView{
public:
	NameView(){}
	
	void set(std::string_view name);
	std::string_view get() const noexcept;

	template<typename OnName>
	void on_name(OnName&& callback){
		on_name_ = callback;
	}

private:
	std::string name_{"Dummy Event"};
	std::function<void(std::string_view)> on_name_{nullptr};
};
}
