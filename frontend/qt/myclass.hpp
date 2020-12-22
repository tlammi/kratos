#pragma once

#include <QObject>
#include <iostream>
#include <QString>

class MyClass: public QObject {
	Q_OBJECT
public:

public slots:
	void my_slot(int row, int column, const QString& msg) const {
		std::cerr << row << ", " << column << ": " << msg.toStdString() << '\n';
	}

};

