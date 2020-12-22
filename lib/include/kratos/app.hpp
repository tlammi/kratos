#pragma once

#include "kratos/event.hpp"
#include <filesystem>
#include <string_view>


namespace kratos{
class App{
public:
	App();

	Event new_event() const ;

	Event load_event(const std::filesystem::path& src);

	void save_event(Event&);

	void save_event_as(Event&, const std::filesystem::path& dst);

private:
};
}
