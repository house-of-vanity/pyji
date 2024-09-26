import sys

# Locals
import config as conf
import ui

def main():
    config = conf.init()
    app = ui.QApplication(sys.argv)
    window = ui.MainWindow(config)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
