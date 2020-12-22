
#include <QGuiApplication>
#include <QQuickView>
#include <QQuickItem>
#include <QQmlApplicationEngine>
#include <thread>
#include <iostream>

#include "myclass.moc"
#include "MutableHeaderTableModel.moc"


using namespace std::literals::chrono_literals;

int main(int argc, char **argv) {
	int res = -1;
	try {
		QGuiApplication app{argc, argv};

		qmlRegisterType<MutableHeaderTableModel>("MutableHeaderTableModel", 0, 1, "MutableHeaderTableModel");

		QQmlApplicationEngine engine("main.qml");
		QObject* root = engine.rootObjects()[0];
		auto name_field = root->findChild<QObject*>("competitorConfigTable");
		MyClass my_class{};
		QObject::connect(name_field, SIGNAL(itemModified(int, int, QString)), &my_class, SLOT(my_slot(int, int, QString)));
		MutableHeaderTableModel* model = root->findChild<MutableHeaderTableModel*>("asd");
		model->insertColumns(0, 2);
		model->setHeaderData(0, Qt::Horizontal,QString("hello"));
		model->setHeaderData(1, Qt::Horizontal, QString("world"));
		model->insertRows(0, 2);

		auto view = root->findChild<QObject*>("asHeader");
		QMetaObject::invokeMethod(view, "forceLayout");
		
		res = app.exec();
	}
	catch (const std::runtime_error &e) {
		std::cerr << e.what() << '\n';
		return 1;
	}
	return res;
}
