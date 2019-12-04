call pyuic5 -o ..\main_view.py main.ui
call pyuic5 -o ..\settings_view.py settings.ui
call pyuic5 -o ..\upload_view.py upload.ui
call pyuic5 -o ..\progress_view.py progress.ui
call pyuic5 -o ..\download_data_view.py download_data.ui
call pyrcc5 -o ..\gui_rc.py gui.qrc
