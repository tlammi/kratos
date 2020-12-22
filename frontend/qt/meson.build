
qt5 = import('qt5')
qt5_deb = dependency('qt5', modules: ['Core', 'Gui', 'Widgets', 'Quick', 'Qml'], method: 'qmake')

qt5_moc_deps = qt5.preprocess(moc_sources: ['myclass.hpp', 'qml/MutableHeaderTableModel.hpp'], include_directories: meson.current_source_dir(), dependencies: qt5_deb)

executable('kratos-qt', 'main.cpp', qt5_moc_deps, link_with : kratos_app, dependencies: [qt5_deb])

