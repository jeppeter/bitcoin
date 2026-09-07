to make cmake ok will add 
SQLITE_INST_DIR=F:\vcpkg\installed\x64-windows

cmake -B build -DCMAKE_PREFIX_PATH=%SQLITE_INST_DIR%

to edit file my_app.vcxproj



copy F:\vcpkg\installed\x64-windows\bin\boost_filesystem-vc143-mt-x64-1_87.dll to .\build\Release to run ok

