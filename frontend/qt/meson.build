
qt5 = import('qt5')
qt5_deb = dependency('qt5', modules: ['Core', 'Gui', 'Widgets', 'Quick', 'Qml'], method: 'qmake')

qml_copy = custom_target('main.qml',
    input:'qml/main.qml', output:'main.qml',
    command: ['python', meson.source_root() / 'script' / 'cp.py', '@INPUT@', '@OUTPUT@'],
    build_by_default: true)

executable('kratos-qt', 'main.cpp', link_with : kratos_app, dependencies: [qt5_deb])

