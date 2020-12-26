#pragma once

#include <qqml.h>

#include <QObject>
#include <QAbstractTableModel>
#include <QVector>
#include <QString>

#include "kratos/table.hpp"

class MutableHeaderTableModel: public QAbstractTableModel {
	Q_OBJECT
	QML_ELEMENT
	QML_ADDED_IN_MINOR_VERSION(1)
public:
	
	void setTable(kratos::Table* tbl){
		QModelIndex parent{};
		beginInsertRows(parent, 0, tbl->height()-1);
		beginInsertColumns(parent, 0, tbl->width()-1);
		tbl_ = tbl;
		endInsertColumns();
		endInsertRows();
	}

	int rowCount(const QModelIndex& = QModelIndex()) const final {
		if(tbl_) return tbl_->height();
		return 0;
	}

	int columnCount(const QModelIndex& = QModelIndex()) const final {
		if(tbl_) return tbl_->width();
		return 0;
	}

	QVariant data(const QModelIndex& index, int role) const final {
		switch(role){
			case Qt::DisplayRole:
				if(tbl_){
					std::string_view str = (*tbl_)[index.row()][index.column()];
					return QString::fromUtf8(str.data(), str.size());
				}
			default:
				break;
		}
		return QVariant();
	}

	Q_INVOKABLE void appendRow(){
		QModelIndex parent{};
		beginInsertRows(parent, tbl_->height(), tbl_->height()); 
		tbl_->append_row();
		endInsertRows();
	}

	Q_INVOKABLE void sort(){
		tbl_->sort_by("Last Name");
		layoutChanged();
	}

	Q_INVOKABLE void set(int x, int y, const QVariant& val){
		(*tbl_)[y][x] = val.toString().toStdString();
	}

	bool setData(const QModelIndex& index, const QVariant& value, int role=Qt::EditRole) final {
		switch(role){
			case Qt::EditRole:
				if(tbl_) (*tbl_)[index.row()][index.column()] = value.toString().toStdString();
				dataChanged(index, index, {role});
				return true;
			default:
				break;
		}
		return false;
	}

	QVariant headerData(int section, Qt::Orientation, int role) const final {
		switch(role){
			case Qt::DisplayRole:
				if(tbl_){
					std::string_view str = tbl_->header().at(section);
					return QString::fromUtf8(str.data(), str.size());
				}
			default:
				break;
		}
		return QVariant();
	}

	bool setHeaderData(int section, Qt::Orientation orientation, const QVariant& data, int role=Qt::EditRole) final {
		switch(role){
			case Qt::EditRole:
				break;
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
		return false;
		/*
		beginInsertRows(parent, row, row+count-1);
		for(auto& column: data_){
			auto iter = column.begin() + row;
			column.insert(iter, count, QVariant{QString{"AAAAAASdf"}});
		}
		endInsertRows();
		return true;
		*/
	}

	bool removeRows(int row, int count, const QModelIndex& parent= QModelIndex()) final {
		return false;
		/*
		beginRemoveRows(parent, row, row+count-1);
		for(auto& column: data_){
			auto begin = column.begin()+row;
			auto end = begin+count;
			column.erase(begin, end);
		}
		endRemoveRows();
		return true;
		*/
	}

	bool insertColumns(int column, int count, const QModelIndex& parent= QModelIndex()) final {
		return false;
		/*
		beginInsertColumns(parent, column, column+count-1);
		auto iter = data_.begin()+column;
		data_.insert(iter, count, {});
		auto hiter = header_data_.begin()+column;
		header_data_.insert(hiter, count, {});
		endInsertColumns();
		return true;
		*/
	}

	bool removeColumns(int column, int count, const QModelIndex& parent= QModelIndex()) final {
		return false;
		/*
		beginRemoveColumns(parent, column, column+count-1);
		auto begin = data_.begin()+column;
		auto end = begin + count;
		data_.erase(begin, end);
		auto hbegin = header_data_.begin()+column;
		auto hend = hbegin + count;
		header_data_.erase(hbegin, hend);
		endRemoveColumns();
		return true;
		*/
	}

private:
	kratos::Table* tbl_{nullptr};
};

