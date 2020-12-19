#include <QGuiApplication>
#include <QQuickView>
#include <QQuickItem>
#include <QQmlApplicationEngine>
#include <thread>
#include <iostream>

using namespace std::literals::chrono_literals;

int main(int argc, char **argv)
{
	int res = -1;
	try
	{
		QGuiApplication app{argc, argv};
		QQmlApplicationEngine engine("main.qml");
		/*QQuickView view;
		view.setSource(QUrl::fromLocalFile("main.qml"));
		view.show();
		QQuickItem *obj = view.rootObject();
		obj->setProperty("width", 500);
		QQuickItem *text = obj->findChild<QQuickItem *>("text");
	for (size_t i = 0; i < 10; ++i)
	{
		std::string tmp = std::to_string(i);
		text->setProperty("text", tmp.c_str());
		std::this_thread::sleep_for(1s);
		app.processEvents();
	}
	*/
		res = app.exec();
	}
	catch (const std::runtime_error &e)
	{
		std::cerr << e.what() << '\n';
		return 1;
	}
	return res;
}
