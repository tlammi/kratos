#include "kratos/nameview.hpp"

namespace kratos{
	

void NameView::set(std::string_view name){
	name_ = name;
	if(on_name_) on_name_(name_);

}

std::string_view NameView::get() const noexcept {
	return name_;
}

}
