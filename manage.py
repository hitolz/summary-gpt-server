from app import creat_app

config_name = 'development'
app = creat_app(config_name)


if __name__ == '__main__':
    app.run()
