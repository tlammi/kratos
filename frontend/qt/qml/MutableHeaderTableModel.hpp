#pragma once

#include <qqml.h>

#include <QObject>
#include <QAbstractTableModel>
#include <QVector>
#include <QString>


class MutableHeaderTableModel: public QAbstractTableModel {
	Q_OBJECT
	QML_ELEMENT
	QML_ADDED_IN_MINOR_VERSION(1)
public:

	int rowCount(const QModelIndex& = QModelIndex()) const final {
		if(data_.size())
			return data_[0].size();
		return 0;
	}

	int columnCount(const QModelIndex& = QModelIndex()) const final {
		return data_.size();
	}

	QVariant data(const QModelIndex& index, int role) const final {
		switch(role){
			case Qt::DisplayRole:
				return data_.at(index.column()).at(index.row());
			default:
				break;
		}
		return QVariant();
	}

	bool setData(const QModelIndex& index, const QVariant& value, int role=Qt::EditRole) final {
		switch(role){
			case Qt::EditRole:
				data_[index.column()][index.row()] = value;
				dataChanged(index, index,{role});
				return true;
			default:
				break;
		}
		return false;
	}

	Q_INVOKABLE QVariant headerData(int section, Qt::Orientation, int role) const final {
		switch(role){
			case Qt::DisplayRole:
				return header_data_.at(section);
			default:
				break;
		}
		return QVariant();
	}

	bool setHeaderData(int section, Qt::Orientation orientation, const QVariant& data, int role=Qt::EditRole) final {
		switch(role){
			case Qt::EditRole:
				header_data_[section] = data;
				headerDataChanged(orientation, section, section);
				return true;
			default:
				break;
		}
		return false;
	}

	Qt::ItemFlags flags(const QModelIndex& index) const final {
		return Qt::ItemIsEditable;
	}


	QHash<int, QByteArray> roleNames() const final {
		return {{Qt::DisplayRole, "display"}};
	}

	bool insertRows(int row, int count, const QModelIndex& parent= QModelIndex()) final {
		beginInsertRows(parent, row, row+count-1);
		for(auto& column: data_){
			auto iter = column.begin() + row;
			column.insert(iter, count, QVariant{QString{"AAAAAASdf"}});
		}
		endInsertRows();
		return true;
	}

	bool removeRows(int row, int count, const QModelIndex& parent= QModelIndex()) final {
		beginRemoveRows(parent, row, row+count-1);
		for(auto& column: data_){
			auto begin = column.begin()+row;
			auto end = begin+count;
			column.erase(begin, end);
		}
		endRemoveRows();
		return true;
	}

	bool insertColumns(int column, int count, const QModelIndex& parent= QModelIndex()) final {
		beginInsertColumns(parent, column, column+count-1);
		auto iter = data_.begin()+column;
		data_.insert(iter, count, {});
		auto hiter = header_data_.begin()+column;
		header_data_.insert(hiter, count, {});
		endInsertColumns();
		return true;
	}

	bool removeColumns(int column, int count, const QModelIndex& parent= QModelIndex()) final {
		beginRemoveColumns(parent, column, column+count-1);
		auto begin = data_.begin()+column;
		auto end = begin + count;
		data_.erase(begin, end);
		auto hbegin = header_data_.begin()+column;
		auto hend = hbegin + count;
		header_data_.erase(hbegin, hend);
		endRemoveColumns();
		return true;
	}

private:
	QVector<QVariant> header_data_{};
	QVector<QVector<QVariant>> data_{};
};

