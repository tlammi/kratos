
#include <QGuiApplication>
#include <QQuickView>
#include <QQuickItem>
#include <QQmlApplicationEngine>
#include <thread>
#include <iostream>

#include "myclass.moc"
#include "MutableHeaderTableModel.moc"

#include "kratos/app.hpp"

using namespace std::literals::chrono_literals;

int main(int argc, char **argv) {
	int res = -1;

	kratos::App app{};

	kratos::Event event = app.new_event();
	try {
		QGuiApplication app{argc, argv};

		qmlRegisterType<MutableHeaderTableModel>("MutableHeaderTableModel", 0, 1, "MutableHeaderTableModel");

		QQmlApplicationEngine engine("main.qml");
		QObject* root = engine.rootObjects()[0];
		auto competitor_config_table = root->findChild<QObject*>("asdf");
		auto model = competitor_config_table->property("model").value<MutableHeaderTableModel*>();

		event.config_table().append_row();
		event.config_table()[0]["Last Name"] = "     Esimerkki     ";
		event.config_table()[0]["First Name"] = "        Erkki         ";

		model->setTable(&event.config_table());

		event.config_table()[0]["Body Weight"] = "80.0kg";

		res = app.exec();
	}
	catch (const std::runtime_error &e) {
		std::cerr << e.what() << '\n';
		return 1;
	}
	return res;
}
