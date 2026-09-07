set INSTDIR=f:\vcpkg\installed\x64-windows

set CURDIR=%~dp0
cmake.exe -B %CURDIR%\build -DCMAKE_PREFIX_PATH=%INSTDIR% -DBUILD_TESTS=OFF && cmake.exe --build %CURDIR%\build --config Release
