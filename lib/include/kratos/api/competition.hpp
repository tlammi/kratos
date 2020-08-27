#pragma once

namespace kratos{
namespace api{
class Competition{
public:
	static Competition create();
	static Competition load(const std::filesystem::path& path);
	void save(const std::filesystem::path& path);

private:
	Competition();
};
}
}
