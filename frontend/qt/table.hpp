#pragma once

#include <QObject>
#include "MutableHeaderTableModel.moc"

class Table{
public:
	Table(QObject* qml_table, size_t column_count);

	template<typename Iter
	void set_columns(Iter iter, Iter end){
		size_t i=0;
		while(iter != end){
			model_->setHeaderData(i, Qt::Horizontal, *iter);
			++i;
			++iter;
		}
	}
	
	size_t columns() const {
		return model_->columnCount();
	}

	size_t rows() const {
		return model_->rowCount();
	}

private:
	QObject* qml_;
	MutableHeaderTableModel* model_{nullptr};
};
