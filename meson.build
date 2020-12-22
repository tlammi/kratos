
project('kratos', 'cpp', default_options: ['cpp_std=c++17'])

add_project_arguments('-I' + meson.source_root() + '/lib/include', language: 'cpp')

subdir('lib/kratos-app')
subdir('frontend/cli')
subdir('frontend/qt')

