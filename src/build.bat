cython meta.py -3 -o meta.c --embed
gcc -I "%userprofile%\AppData\Local\Programs\Python\Python38\include" -L "%userprofile%\AppData\Local\Programs\Python\Python38\libs" -DMS_WIN64 meta.c -lpython38 -lm -municode -o meta.exe
del meta.c
del __*
