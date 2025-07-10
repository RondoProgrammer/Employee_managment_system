from app import create_app

app = create_app()

if __name__ == '__main__':    #Runs this code only if file run.py is being run directly (not imported).”
    app.run(debug=True)       #debug=True enables:
                                #Hot reloading (restarts the server when you change code)
                                #Detailed error pages for debugging
