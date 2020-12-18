
qt5 = import('qt5')
qt5_deb = dependency('qt5', modules: ['Core', 'Gui', 'Widgets'], method: 'qmake')
executable('kratos-qt', 'main.cpp', link_with : kratos_app, dependencies: qt5_deb)

