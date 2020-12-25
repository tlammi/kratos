
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

		const auto& header = event.config_table().header();

		model->insertColumns(0, header.size());
		for(size_t i=0; i < header.size(); ++i){
			model->setHeaderData(i, Qt::Horizontal, QString::fromUtf8(header[i].data(), header[i].size()));
		}
		/*
		model->setHeaderData(0, Qt::Horizontal, "hello");
		model->setHeaderData(1, Qt::Horizontal, "world");
		*/
		//model->insertRows(0, header.size());
		model->insertRows(0, 2);
		res = app.exec();
	}
	catch (const std::runtime_error &e) {
		std::cerr << e.what() << '\n';
		return 1;
	}
	return res;
}
